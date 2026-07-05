from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from typing import Protocol

from domain.service_scale.services.eligibility_reason import EligibilityReason
from domain.service_scale.specifications.eligibility_context import EligibilityContext
from domain.service_scale.specifications.has_minimum_rest import HasMinimumRestSpecification
from domain.service_scale.specifications.has_no_service_conflict import HasNoServiceConflictSpecification
from domain.service_scale.specifications.is_active import MilitaryActiveSpecification
from domain.service_scale.specifications.is_not_already_assigned import (
    MilitaryNotAlreadyAssignedSpecification,
)
from domain.service_scale.specifications.is_not_manually_blocked import (
    MilitaryNotManuallyBlockedSpecification,
)
from domain.service_scale.specifications.is_not_on_leave import MilitaryNotOnLeaveSpecification
from domain.service_scale.specifications.is_not_restricted import MilitaryNotRestrictedSpecification
from domain.service_scale.specifications.is_role_qualified import MilitaryQualifiedForRoleSpecification
from domain.service_scale.specifications.is_scale_compatible import MilitaryCompatibleScaleSpecification
from shared.kernel.identity import Identity


class EligibilitySpecification(Protocol):
    """Protocol implemented by eligibility specifications."""

    reason: EligibilityReason

    def is_satisfied_by(self, candidate: EligibilityContext) -> bool:
        """Return whether candidate satisfies this specification."""
        raise NotImplementedError


@dataclass(frozen=True, slots=True)
class EligibilityPolicyConfiguration:
    """Configuration used by the eligibility policy."""

    allowed_role_ids_by_military: Mapping[Identity, frozenset[Identity]]
    allowed_scale_ids_by_military: Mapping[Identity, frozenset[Identity]]
    manually_blocked_military_ids: frozenset[Identity]
    allow_one_by_one_exception: bool = False


class EligibilityPolicy:
    """Policy that executes the complete eligibility specification pipeline."""

    def __init__(
        self,
        specifications: Iterable[EligibilitySpecification] | None = None,
        configuration: EligibilityPolicyConfiguration | None = None,
    ) -> None:
        self._specifications = tuple(specifications or self._default_specifications())
        self._configuration = configuration or EligibilityPolicyConfiguration(
            allowed_role_ids_by_military={},
            allowed_scale_ids_by_military={},
            manually_blocked_military_ids=frozenset(),
        )

    @property
    def configuration(self) -> EligibilityPolicyConfiguration:
        """Return policy configuration."""
        return self._configuration

    def evaluate(self, context: EligibilityContext) -> tuple[EligibilityReason, ...]:
        """Execute every specification and return all failure reasons."""
        reasons: list[EligibilityReason] = []
        for specification in self._specifications:
            if not specification.is_satisfied_by(context):
                reasons.append(specification.reason)
        return tuple(reasons)

    @staticmethod
    def _default_specifications() -> tuple[EligibilitySpecification, ...]:
        """Return default eligibility pipeline ordering."""
        return (
            MilitaryActiveSpecification(),
            MilitaryNotOnLeaveSpecification(),
            MilitaryNotRestrictedSpecification(),
            HasMinimumRestSpecification(),
            MilitaryQualifiedForRoleSpecification(),
            MilitaryCompatibleScaleSpecification(),
            HasNoServiceConflictSpecification(),
            MilitaryNotAlreadyAssignedSpecification(),
            MilitaryNotManuallyBlockedSpecification(),
        )
