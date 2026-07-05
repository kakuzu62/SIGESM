from __future__ import annotations

from collections.abc import Hashable
import re

from domain.military.exceptions import InvalidMilitaryIdException
from shared.kernel.value_object import ValueObject


class MilitaryId(ValueObject):
    """Normalized non-empty military identifier."""

    __slots__ = ("_value",)
    _value: str

    def __init__(self, value: str) -> None:
        normalized = re.sub(r"\s+", "", value).upper()
        if not normalized:
            raise InvalidMilitaryIdException("Military id cannot be empty.")

        object.__setattr__(self, "_value", normalized)
        super().__init__()

    @property
    def value(self) -> str:
        """Return the normalized military identifier."""
        return self._value

    @property
    def equality_components(self) -> tuple[Hashable, ...]:
        """Return values that define equality."""
        return (self._value,)

    def __str__(self) -> str:
        return self._value
