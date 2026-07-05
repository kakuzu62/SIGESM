from __future__ import annotations

from collections.abc import Hashable
import re

from domain.military.exceptions import InvalidFullNameException
from shared.kernel.value_object import ValueObject


class FullName(ValueObject):
    """Complete human name with at least two meaningful words."""

    __slots__ = ("_value",)
    _value: str

    def __init__(self, value: str) -> None:
        normalized = re.sub(r"\s+", " ", value).strip()
        parts = normalized.split(" ")

        if len(parts) < 2 or any(len(part) < 2 for part in parts):
            raise InvalidFullNameException("Full name must contain at least first and last name.")

        object.__setattr__(self, "_value", normalized)
        super().__init__()

    @property
    def value(self) -> str:
        """Return the normalized full name."""
        return self._value

    @property
    def equality_components(self) -> tuple[Hashable, ...]:
        """Return values that define equality."""
        return (self._value.casefold(),)

    def __str__(self) -> str:
        return self._value
