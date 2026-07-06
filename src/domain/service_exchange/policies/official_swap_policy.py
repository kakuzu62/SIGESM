from __future__ import annotations

from dataclasses import dataclass

from domain.military.entities import MilitaryPerson
from domain.service_exchange.entities import OfficialSwap
from domain.service_scale.entities import ServiceAssignment, ServiceRole, ServiceScale
from domain.service_scale.policies.eligibility_policy import (
    EligibilityPolicy,
    EligibilityPolicyConfiguration,
)
from domain.service_scale.services.eligibility_engine import EligibilityEngine
from domain.service_scale.services.eligibility_reason import EligibilityReason


@dataclass(frozen=True, slots=True)
class OfficialSwapPolicy:
    """Policy that validates both sides of an official service swap."""

    allow_formal_rest_exception: bool = False

    def evaluate(
        self,
        swap: OfficialSwap,
        source_military: MilitaryPerson,
        target_military: MilitaryPerson,
        service_scale: ServiceScale,
        source_role: ServiceRole,
        target_role: ServiceRole,
        history: tuple[ServiceAssignment, ...],
    ) -> tuple[EligibilityReason, ...]:
        """Return all reasons that prevent an official swap approval."""
        policy = EligibilityPolicy(
            configuration=EligibilityPolicyConfiguration(
                allowed_role_ids_by_military={},
                allowed_scale_ids_by_military={},
                manually_blocked_military_ids=frozenset(),
                allow_one_by_one_exception=self.allow_formal_rest_exception,
            )
        )
        engine = EligibilityEngine(policy)
        target_on_source_day = engine.evaluate(
            military=target_military,
            service_scale=service_scale,
            service_role=source_role,
            history=history,
            service_date=swap.source_assignment.service_date,
        )
        source_on_target_day = engine.evaluate(
            military=source_military,
            service_scale=service_scale,
            service_role=target_role,
            history=history,
            service_date=swap.target_assignment.service_date,
        )
        return target_on_source_day.reasons + source_on_target_day.reasons
