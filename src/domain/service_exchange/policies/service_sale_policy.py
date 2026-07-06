from __future__ import annotations

from dataclasses import dataclass

from domain.military.entities import MilitaryPerson
from domain.service_exchange.entities import ServiceSale
from domain.service_scale.entities import ServiceAssignment, ServiceRole, ServiceScale
from domain.service_scale.policies.eligibility_policy import (
    EligibilityPolicy,
    EligibilityPolicyConfiguration,
)
from domain.service_scale.services.eligibility_engine import EligibilityEngine
from domain.service_scale.services.eligibility_reason import EligibilityReason


@dataclass(frozen=True, slots=True)
class ServiceSalePolicy:
    """Policy that validates operational eligibility for a service sale buyer."""

    allow_formal_rest_exception: bool = False

    def evaluate(
        self,
        sale: ServiceSale,
        buyer: MilitaryPerson,
        service_scale: ServiceScale,
        seller_role: ServiceRole,
        history: tuple[ServiceAssignment, ...],
    ) -> tuple[EligibilityReason, ...]:
        """Return all reasons that prevent a service sale approval."""
        policy = EligibilityPolicy(
            configuration=EligibilityPolicyConfiguration(
                allowed_role_ids_by_military={},
                allowed_scale_ids_by_military={},
                manually_blocked_military_ids=frozenset(),
                allow_one_by_one_exception=self.allow_formal_rest_exception,
            )
        )
        result = EligibilityEngine(policy).evaluate(
            military=buyer,
            service_scale=service_scale,
            service_role=seller_role,
            history=history,
            service_date=sale.seller_assignment.service_date,
        )
        return result.reasons
