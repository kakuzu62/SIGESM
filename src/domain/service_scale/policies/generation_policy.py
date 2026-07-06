from __future__ import annotations

import logging
from dataclasses import dataclass
from time import perf_counter

from domain.military.entities import MilitaryPerson
from domain.service_scale.engines.generation_context import GenerationContext
from domain.service_scale.engines.generation_statistics import GenerationStatistics
from domain.service_scale.events import MilitarySelected, MilitarySkipped, ScaleGenerated
from domain.service_scale.policies.eligibility_policy import (
    EligibilityPolicy,
    EligibilityPolicyConfiguration,
)
from domain.service_scale.policies.fairness_policy import FairnessPolicy
from domain.service_scale.services.candidate_selector import CandidateSelector
from domain.service_scale.strategies import BlackScaleStrategy, RedScaleStrategy, ScaleStrategy
from domain.service_scale.value_objects import ScaleType
from shared.kernel.domain_event import DomainEvent
from shared.kernel.identity import Identity

logger = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class GenerationPolicyResult:
    """Internal result produced by the generation policy pipeline."""

    selected: tuple[MilitaryPerson, ...]
    skipped_events: tuple[MilitarySkipped, ...]
    statistics: GenerationStatistics
    events: tuple[DomainEvent, ...]
    elapsed_seconds: float


class GenerationPolicy:
    """Policy that executes the scale generation pipeline."""

    def __init__(
        self,
        candidate_selector: CandidateSelector | None = None,
        fairness_policy: FairnessPolicy | None = None,
        strategies: dict[ScaleType, ScaleStrategy] | None = None,
    ) -> None:
        self._candidate_selector = candidate_selector or CandidateSelector()
        self._fairness_policy = fairness_policy or FairnessPolicy()
        self._strategies = strategies or {
            ScaleType.PRETA: BlackScaleStrategy(),
            ScaleType.VERMELHA: RedScaleStrategy(),
        }

    def generate(
        self, generation_id: Identity, context: GenerationContext
    ) -> GenerationPolicyResult:
        """Execute candidate search, eligibility, fairness ordering and selection."""
        started_at = perf_counter()
        logger.info(
            "Iniciando geracao de escala id=%s data=%s escala=%s candidatos=%s parametros=%s",
            generation_id,
            context.service_date,
            context.scale_type.value,
            len(context.eligible_military),
            dict(context.parameters),
        )
        eligibility_policy = EligibilityPolicy(
            configuration=EligibilityPolicyConfiguration(
                allowed_role_ids_by_military=context.restrictions.get(
                    "allowed_role_ids_by_military", {}
                ),
                allowed_scale_ids_by_military=context.restrictions.get(
                    "allowed_scale_ids_by_military", {}
                ),
                manually_blocked_military_ids=context.blocked_military_ids,
                allow_one_by_one_exception=context.allow_one_by_one_exception,
            )
        )
        selection = self._candidate_selector.select(context, eligibility_policy)
        fair_order = self._fairness_policy.order(
            selection.eligible, context.service_date, context.history
        )
        strategy = self._strategies[context.scale_type]
        ordered = strategy.apply(context, fair_order)
        selected = ordered[: context.selection_limit]
        elapsed = perf_counter() - started_at
        skipped_events = tuple(
            MilitarySkipped(
                generation_id=generation_id,
                military_id=skipped.military_id,
                scale_type=context.scale_type,
                service_date=context.service_date.value,
                reasons=skipped.reasons,
            )
            for skipped in selection.skipped
        )
        selected_events = tuple(
            MilitarySelected(
                generation_id=generation_id,
                military_id=military.id,
                scale_type=context.scale_type,
                service_date=context.service_date.value,
            )
            for military in selected
        )
        generated_event = ScaleGenerated(
            generation_id=generation_id,
            scale_id=context.service_scale.id,
            scale_type=context.scale_type,
            service_date=context.service_date.value,
            selected_count=len(selected),
        )
        statistics = GenerationStatistics(
            analyzed_count=len(context.eligible_military),
            eligible_count=len(selection.eligible),
            skipped_count=len(selection.skipped),
            selected_count=len(selected),
            execution_time_seconds=elapsed,
            verification_count=selection.verification_count,
        )
        logger.info(
            "Geracao concluida id=%s analisados=%s elegiveis=%s descartados=%s selecionados=%s tempo=%.6fs",
            generation_id,
            statistics.analyzed_count,
            statistics.eligible_count,
            statistics.skipped_count,
            statistics.selected_count,
            elapsed,
        )
        return GenerationPolicyResult(
            selected=selected,
            skipped_events=skipped_events,
            statistics=statistics,
            events=selected_events + skipped_events + (generated_event,),
            elapsed_seconds=elapsed,
        )
