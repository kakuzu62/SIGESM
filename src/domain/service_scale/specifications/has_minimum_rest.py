from __future__ import annotations

from datetime import datetime, time, timedelta

from domain.service_scale.policies.minimum_rest_policy import MinimumRestPolicy
from domain.service_scale.services.eligibility_reason import EligibilityReason
from domain.service_scale.specifications.eligibility_context import EligibilityContext
from domain.service_scale.value_objects import AssignmentStatus, RestPeriod


class HasMinimumRestSpecification:
    """Specification that validates minimum rest before a new service."""

    reason = EligibilityReason.INSUFFICIENT_REST

    def __init__(self, policy: MinimumRestPolicy | None = None) -> None:
        self._policy = policy or MinimumRestPolicy()

    def is_satisfied_by(self, candidate: EligibilityContext) -> bool:
        """Return whether the candidate has enough rest since the last service."""
        previous_assignments = tuple(
            assignment
            for assignment in candidate.history
            if assignment.military_id == candidate.military.id
            and assignment.status in {AssignmentStatus.SCHEDULED, AssignmentStatus.COMPLETED}
            and assignment.service_date.value < candidate.service_date.value
        )
        if not previous_assignments:
            return True

        latest_assignment = max(
            previous_assignments, key=lambda assignment: assignment.service_date.value
        )
        rest_start = datetime.combine(latest_assignment.service_date.value, time.min) + timedelta(
            hours=24
        )
        rest_hours = int(
            (datetime.combine(candidate.service_date.value, time.min) - rest_start).total_seconds()
            // 3600
        )
        return self._policy.is_satisfied(
            RestPeriod(max(rest_hours, 0)),
            allow_one_by_one_exception=candidate.allow_one_by_one_exception,
        )
