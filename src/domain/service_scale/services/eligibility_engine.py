from __future__ import annotations

import logging
from time import perf_counter
from typing import Any

from domain.military.entities import MilitaryPerson
from domain.service_scale.entities import ServiceAssignment, ServiceRole, ServiceScale
from domain.service_scale.events import MilitaryDeclaredEligible, MilitaryDeclaredIneligible
from domain.service_scale.policies.eligibility_policy import EligibilityPolicy
from domain.service_scale.services.eligibility_result import EligibilityResult
from domain.service_scale.specifications.eligibility_context import EligibilityContext
from domain.service_scale.value_objects import ServiceDate
from shared.kernel.domain_event import DomainEvent

logger = logging.getLogger(__name__)


class EligibilityEngine:
    """Domain service that evaluates military eligibility for service scale assignment."""

    def __init__(self, policy: EligibilityPolicy | None = None) -> None:
        self._policy = policy or EligibilityPolicy()
        self._domain_events: list[DomainEvent] = []

    def evaluate(
        self,
        military: MilitaryPerson,
        service_scale: ServiceScale,
        service_role: ServiceRole,
        history: tuple[ServiceAssignment, ...],
        service_date: ServiceDate,
    ) -> EligibilityResult:
        """Evaluate whether a military person can assume a service on a date."""
        started_at = perf_counter()
        configuration = self._policy.configuration
        context = EligibilityContext(
            military=military,
            service_scale=service_scale,
            service_role=service_role,
            history=history,
            service_date=service_date,
            allowed_role_ids_by_military=configuration.allowed_role_ids_by_military,
            allowed_scale_ids_by_military=configuration.allowed_scale_ids_by_military,
            manually_blocked_military_ids=configuration.manually_blocked_military_ids,
            allow_one_by_one_exception=configuration.allow_one_by_one_exception,
        )
        reasons = self._policy.evaluate(context)
        elapsed = perf_counter() - started_at
        metadata: dict[str, Any] = {
            "military_id": str(military.id),
            "service_date": str(service_date),
            "scale_type": service_scale.scale_type.value,
            "scale_id": str(service_scale.id),
            "role_id": str(service_role.id),
            "elapsed_seconds": elapsed,
        }
        result = EligibilityResult.create(reasons=reasons, metadata=metadata)
        self._record_event(military, service_scale, service_date, result)
        self._log_result(military, service_scale, service_date, result, elapsed)
        return result

    def pull_domain_events(self) -> tuple[DomainEvent, ...]:
        """Return generated eligibility domain events and clear the internal buffer."""
        events = tuple(self._domain_events)
        self._domain_events.clear()
        return events

    def _record_event(
        self,
        military: MilitaryPerson,
        service_scale: ServiceScale,
        service_date: ServiceDate,
        result: EligibilityResult,
    ) -> None:
        if result.eligible:
            self._domain_events.append(
                MilitaryDeclaredEligible(
                    military_id=military.id,
                    scale_id=service_scale.id,
                    scale_type=service_scale.scale_type,
                    service_date=service_date.value,
                )
            )
            return

        self._domain_events.append(
            MilitaryDeclaredIneligible(
                military_id=military.id,
                scale_id=service_scale.id,
                scale_type=service_scale.scale_type,
                service_date=service_date.value,
                reasons=result.reasons,
            )
        )

    def _log_result(
        self,
        military: MilitaryPerson,
        service_scale: ServiceScale,
        service_date: ServiceDate,
        result: EligibilityResult,
        elapsed: float,
    ) -> None:
        logger.info(
            "Elegibilidade avaliada militar=%s data=%s escala=%s resultado=%s motivos=%s tempo=%.6fs",
            military.military_id.value,
            service_date,
            service_scale.scale_type.value,
            result.eligible,
            tuple(reason.value for reason in result.reasons),
            elapsed,
        )
