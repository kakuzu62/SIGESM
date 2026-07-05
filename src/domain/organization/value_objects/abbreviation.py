from __future__ import annotations

from collections.abc import Hashable
import re

from domain.organization.exceptions import InvalidAbbreviationException
from shared.kernel.value_object import ValueObject


class Abbreviation(ValueObject):
    """Short organization abbreviation."""

    __slots__ = ("_value",)
    _value: str

    def __init__(self, value: str) -> None:
        normalized = re.sub(r"\s+", "", value).upper()
        if not normalized or len(normalized) > 20:
            raise InvalidAbbreviationException("Abbreviation must have 1 to 20 non-empty characters.")

        object.__setattr__(self, "_value", normalized)
        super().__init__()

    @property
    def value(self) -> str:
        """Return the normalized abbreviation."""
        return self._value

    @property
    def equality_components(self) -> tuple[Hashable, ...]:
        """Return values that define equality."""
        return (self._value,)

    def __str__(self) -> str:
        return self._value
