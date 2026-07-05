from __future__ import annotations

from domain.service_scale.services.eligibility_reason import EligibilityReason
from domain.service_scale.specifications.eligibility_context import EligibilityContext
from domain.service_scale.value_objects import AssignmentStatus


class MilitaryNotAlreadyAssignedSpecification:
    """Specification that rejects duplicate assignment inside the target scale."""

    reason = EligibilityReason.ALREADY_ASSIGNED

    def is_satisfied_by(self, candidate: EligibilityContext) -> bool:
        """Return whether the military person is not already assigned in this scale/date."""
        return not any(
            assignment.military_id == candidate.military.id
            and assignment.service_date == candidate.service_date
            and assignment.status == AssignmentStatus.SCHEDULED
            for assignment in candidate.service_scale.assignments
        )
