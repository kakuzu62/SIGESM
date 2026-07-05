from __future__ import annotations

from domain.service_scale.services.eligibility_reason import EligibilityReason
from domain.service_scale.specifications.eligibility_context import EligibilityContext
from domain.service_scale.value_objects import AssignmentStatus


class HasNoServiceConflictSpecification:
    """Specification that rejects same-date service conflicts."""

    reason = EligibilityReason.SERVICE_CONFLICT

    def is_satisfied_by(self, candidate: EligibilityContext) -> bool:
        """Return whether the military person has no active same-date conflict."""
        return not any(
            assignment.military_id == candidate.military.id
            and assignment.service_date == candidate.service_date
            and assignment.status in {AssignmentStatus.SCHEDULED, AssignmentStatus.COMPLETED}
            for assignment in candidate.history
        )
