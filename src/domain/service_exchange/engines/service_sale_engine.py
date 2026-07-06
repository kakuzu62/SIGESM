from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Mapping

from domain.military.entities import MilitaryPerson
from domain.service_exchange.entities import ServiceSale
from domain.service_exchange.policies.service_sale_policy import ServiceSalePolicy
from domain.service_scale.entities import ServiceAssignment, ServiceRole, ServiceScale
from domain.service_scale.services.eligibility_reason import EligibilityReason
from shared.kernel.identity import Identity


@dataclass(frozen=True, slots=True)
class ServiceSaleDecision:
    """Auditable decision returned by service sale validation."""

    approved: bool
    reasons: tuple[EligibilityReason, ...]
    warnings: tuple[str, ...]
    metadata: Mapping[str, Any]


class ServiceSaleEngine:
    """Domain service that validates service sale operations."""

    def __init__(self, policy: ServiceSalePolicy | None = None) -> None:
        self._policy = policy or ServiceSalePolicy()

    def evaluate(
        self,
        sale: ServiceSale,
        buyer: MilitaryPerson,
        service_scale: ServiceScale,
        seller_role: ServiceRole,
        history: tuple[ServiceAssignment, ...],
        decided_by: Identity,
    ) -> ServiceSaleDecision:
        """Evaluate and apply a service sale decision."""
        reasons = self._policy.evaluate(
            sale=sale,
            buyer=buyer,
            service_scale=service_scale,
            seller_role=seller_role,
            history=history,
        )
        metadata: dict[str, Any] = {
            "sale_id": str(sale.id),
            "seller_military_id": str(sale.seller_assignment.military_id),
            "buyer_military_id": str(buyer.id),
            "sold_service_date": str(sale.seller_assignment.service_date),
            "buyer_original_service_date": str(sale.buyer_assignment.service_date),
            "buyer_counter_preserved": True,
            "seller_counter_resets_normally": not reasons,
            "buyer_extraordinary_service": not reasons,
        }
        if reasons:
            sale.reject(tuple(reason.value for reason in reasons))
        else:
            sale.approve(decided_by)

        return ServiceSaleDecision(
            approved=not reasons,
            reasons=reasons,
            warnings=(),
            metadata=MappingProxyType(metadata),
        )
