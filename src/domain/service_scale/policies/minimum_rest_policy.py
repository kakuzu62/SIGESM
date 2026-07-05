from __future__ import annotations

from domain.service_scale.value_objects import RestPeriod


class MinimumRestPolicy:
    """Policy that evaluates standard rest and controlled 1x1 exceptions."""

    def __init__(self, minimum_hours: int = 78, one_by_one_minimum_hours: int = 24) -> None:
        self._minimum_hours = minimum_hours
        self._one_by_one_minimum_hours = one_by_one_minimum_hours

    @property
    def minimum_hours(self) -> int:
        """Return default minimum rest hours."""
        return self._minimum_hours

    @property
    def one_by_one_minimum_hours(self) -> int:
        """Return minimum hours allowed by the controlled 1x1 exception."""
        return self._one_by_one_minimum_hours

    def is_satisfied(self, rest_period: RestPeriod, allow_one_by_one_exception: bool = False) -> bool:
        """Return whether rest period satisfies the policy."""
        if rest_period.hours >= self._minimum_hours:
            return True

        return allow_one_by_one_exception and rest_period.hours >= self._one_by_one_minimum_hours
