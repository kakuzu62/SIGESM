from __future__ import annotations

from collections.abc import Hashable
from datetime import date, datetime, time

from domain.service_scale.exceptions import InvalidServiceDateException
from shared.kernel.value_object import ValueObject


class ServiceDate(ValueObject):
    """Date of a 24-hour service shift."""

    __slots__ = ("_value",)
    _value: date

    def __init__(self, value: date) -> None:
        if not isinstance(value, date):
            raise InvalidServiceDateException("Service date must be a valid date.")
        object.__setattr__(self, "_value", value)
        super().__init__()

    @property
    def value(self) -> date:
        """Return the service date."""
        return self._value

    @property
    def starts_at(self) -> datetime:
        """Return service start datetime."""
        return datetime.combine(self._value, time.min)

    @property
    def ends_at(self) -> datetime:
        """Return service end datetime for a 24-hour service."""
        return datetime.combine(self._value, time.max)

    @property
    def equality_components(self) -> tuple[Hashable, ...]:
        """Return values that define equality."""
        return (self._value,)

    def __str__(self) -> str:
        return self._value.isoformat()
