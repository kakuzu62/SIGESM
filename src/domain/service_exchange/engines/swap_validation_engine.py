from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Mapping

from domain.military.entities import MilitaryPerson
from domain.service_exchange.entities import OfficialSwap
from domain.service_exchange.policies.official_swap_policy import OfficialSwapPolicy
from domain.service_scale.entities import ServiceAssignment, ServiceRole, ServiceScale
from domain.service_scale.services.eligibility_reason import EligibilityReason
from shared.kernel.identity import Identity


@dataclass(frozen=True, slots=True)
class SwapDecision:
    """Auditable decision returned by official swap validation."""

    approved: bool
    reasons: tuple[EligibilityReason, ...]
    warnings: tuple[str, ...]
    metadata: Mapping[str, Any]


class SwapValidationEngine:
    """Domain service that validates official service swaps."""

    def __init__(self, policy: OfficialSwapPolicy | None = None) -> None:
        self._policy = policy or OfficialSwapPolicy()

    def evaluate(
        self,
        swap: OfficialSwap,
        source_military: MilitaryPerson,
        target_military: MilitaryPerson,
        service_scale: ServiceScale,
        source_role: ServiceRole,
        target_role: ServiceRole,
        history: tuple[ServiceAssignment, ...],
        decided_by: Identity,
    ) -> SwapDecision:
        """Evaluate and apply an official swap decision."""
        reasons = self._policy.evaluate(
            swap=swap,
            source_military=source_military,
            target_military=target_military,
            service_scale=service_scale,
            source_role=source_role,
            target_role=target_role,
            history=history,
        )
        metadata: dict[str, Any] = {
            "swap_id": str(swap.id),
            "source_military_id": str(source_military.id),
            "target_military_id": str(target_military.id),
            "source_service_date": str(swap.source_assignment.service_date),
            "target_service_date": str(swap.target_assignment.service_date),
            "formal_rest_exception": self._policy.allow_formal_rest_exception,
        }
        if reasons:
            swap.reject(tuple(reason.value for reason in reasons))
        else:
            swap.approve(decided_by)

        return SwapDecision(
            approved=not reasons,
            reasons=reasons,
            warnings=(),
            metadata=MappingProxyType(metadata),
        )
