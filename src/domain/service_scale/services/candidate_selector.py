from __future__ import annotations

from dataclasses import dataclass

from domain.military.entities import MilitaryPerson
from domain.service_scale.engines.generation_context import GenerationContext
from domain.service_scale.engines.generation_result import SkippedCandidate
from domain.service_scale.policies.eligibility_policy import EligibilityPolicy
from domain.service_scale.services.eligibility_engine import EligibilityEngine


@dataclass(frozen=True, slots=True)
class CandidateSelection:
    """Candidates accepted and skipped by the eligibility pipeline."""

    eligible: tuple[MilitaryPerson, ...]
    skipped: tuple[SkippedCandidate, ...]
    verification_count: int


class CandidateSelector:
    """Domain service responsible for ordering, filtering and checking candidates."""

    def select(self, context: GenerationContext, policy: EligibilityPolicy) -> CandidateSelection:
        """Return candidates approved by eligibility evaluation."""
        eligible: list[MilitaryPerson] = []
        skipped: list[SkippedCandidate] = []
        ordered_candidates = tuple(sorted(context.eligible_military, key=lambda candidate: str(candidate.id)))
        for military in ordered_candidates:
            if military.id in context.blocked_military_ids:
                continue

            result = EligibilityEngine(policy).evaluate(
                military=military,
                service_scale=context.service_scale,
                service_role=context.service_role,
                history=context.history,
                service_date=context.service_date,
            )
            if result.eligible:
                eligible.append(military)
            else:
                skipped.append(SkippedCandidate(military_id=military.id, reasons=result.reasons))

        return CandidateSelection(
            eligible=tuple(eligible),
            skipped=tuple(skipped),
            verification_count=len(ordered_candidates),
        )
