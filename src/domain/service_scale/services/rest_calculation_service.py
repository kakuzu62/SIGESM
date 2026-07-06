from __future__ import annotations

from datetime import datetime, time, timedelta

from domain.service_scale.entities import ServiceAssignment
from domain.service_scale.policies.minimum_rest_policy import MinimumRestPolicy
from domain.service_scale.value_objects import AssignmentStatus, RestPeriod, ServiceDate
from shared.kernel.identity import Identity


class RestCalculationService:
    """Domain service responsible for rest calculations between assignments."""

    def __init__(self, policy: MinimumRestPolicy | None = None) -> None:
        self._policy = policy or MinimumRestPolicy()

    def calculate_rest(
        self,
        military_id: Identity,
        service_date: ServiceDate,
        history: tuple[ServiceAssignment, ...],
    ) -> RestPeriod:
        """Calculate rest hours since the latest previous service."""
        previous = tuple(
            assignment
            for assignment in history
            if assignment.military_id == military_id
            and assignment.service_date.value < service_date.value
            and assignment.status in {AssignmentStatus.SCHEDULED, AssignmentStatus.COMPLETED}
        )
        if not previous:
            return RestPeriod(self._policy.minimum_hours)

        latest = max(previous, key=lambda assignment: assignment.service_date.value)
        rest_start = datetime.combine(latest.service_date.value, time.min) + timedelta(hours=24)
        rest_hours = int(
            (datetime.combine(service_date.value, time.min) - rest_start).total_seconds() // 3600
        )
        return RestPeriod(max(rest_hours, 0))

    def has_minimum_rest(
        self,
        rest_period: RestPeriod,
        allow_one_by_one_exception: bool = False,
    ) -> bool:
        """Return whether a rest period satisfies the configured policy."""
        return self._policy.is_satisfied(rest_period, allow_one_by_one_exception)

    def next_available_date(
        self,
        service_date: ServiceDate,
        allow_one_by_one_exception: bool = False,
    ) -> ServiceDate:
        """Calculate next date available after a 24-hour service."""
        rest_hours = (
            self._policy.one_by_one_minimum_hours
            if allow_one_by_one_exception
            else self._policy.minimum_hours
        )
        next_datetime = datetime.combine(service_date.value, time.min) + timedelta(
            hours=24 + rest_hours
        )
        return ServiceDate(next_datetime.date())
