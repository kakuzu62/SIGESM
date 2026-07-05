from __future__ import annotations

from collections.abc import Hashable
from dataclasses import dataclass

from domain.service_scale.exceptions import InvalidRestPeriodException
from shared.kernel.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class RestPeriodPolicySettings:
    """Settings used to evaluate minimum rest periods."""

    minimum_hours: int = 78
    one_by_one_minimum_hours: int = 24


class RestPeriod(ValueObject):
    """Rest period between service assignments measured in hours."""

    __slots__ = ("_hours",)
    _hours: int
    DEFAULT_MINIMUM_HOURS = 78
    ONE_BY_ONE_MINIMUM_HOURS = 24

    def __init__(self, hours: int) -> None:
        if hours < 0:
            raise InvalidRestPeriodException("Rest period cannot be negative.")
        object.__setattr__(self, "_hours", hours)
        super().__init__()

    @classmethod
    def standard_minimum(cls) -> RestPeriod:
        """Return the standard minimum rest period."""
        return cls(cls.DEFAULT_MINIMUM_HOURS)

    @property
    def hours(self) -> int:
        """Return rest period in hours."""
        return self._hours

    def satisfies_standard_minimum(self) -> bool:
        """Return whether this period satisfies the default 78-hour rest."""
        return self._hours >= self.DEFAULT_MINIMUM_HOURS

    def satisfies_one_by_one_exception(self) -> bool:
        """Return whether this period satisfies the controlled 1x1 exception floor."""
        return self._hours >= self.ONE_BY_ONE_MINIMUM_HOURS

    @property
    def equality_components(self) -> tuple[Hashable, ...]:
        """Return values that define equality."""
        return (self._hours,)
