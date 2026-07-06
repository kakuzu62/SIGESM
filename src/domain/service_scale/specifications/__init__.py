"""Service scale specifications."""

from domain.service_scale.specifications.military_available_for_scale import (
    MilitaryAvailableForScaleSpecification,
)
from domain.service_scale.specifications.minimum_rest_satisfied import (
    MinimumRestSatisfiedSpecification,
)
from domain.service_scale.specifications.has_minimum_rest import HasMinimumRestSpecification
from domain.service_scale.specifications.has_no_service_conflict import (
    HasNoServiceConflictSpecification,
)
from domain.service_scale.specifications.is_active import MilitaryActiveSpecification
from domain.service_scale.specifications.is_not_already_assigned import (
    MilitaryNotAlreadyAssignedSpecification,
)
from domain.service_scale.specifications.is_not_manually_blocked import (
    MilitaryNotManuallyBlockedSpecification,
)
from domain.service_scale.specifications.is_not_on_leave import MilitaryNotOnLeaveSpecification
from domain.service_scale.specifications.is_not_restricted import MilitaryNotRestrictedSpecification
from domain.service_scale.specifications.is_role_qualified import (
    MilitaryQualifiedForRoleSpecification,
)
from domain.service_scale.specifications.is_scale_compatible import (
    MilitaryCompatibleScaleSpecification,
)

__all__ = [
    "HasMinimumRestSpecification",
    "HasNoServiceConflictSpecification",
    "MilitaryActiveSpecification",
    "MilitaryAvailableForScaleSpecification",
    "MilitaryCompatibleScaleSpecification",
    "MilitaryNotAlreadyAssignedSpecification",
    "MilitaryNotManuallyBlockedSpecification",
    "MilitaryNotOnLeaveSpecification",
    "MilitaryNotRestrictedSpecification",
    "MilitaryQualifiedForRoleSpecification",
    "MinimumRestSatisfiedSpecification",
]
