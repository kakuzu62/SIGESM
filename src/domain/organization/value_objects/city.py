from __future__ import annotations

from collections.abc import Hashable
import re

from domain.organization.exceptions import InvalidLocationException
from shared.kernel.value_object import ValueObject


class City(ValueObject):
    """City where an organization is located."""

    __slots__ = ("_value",)
    _value: str

    def __init__(self, value: str) -> None:
        normalized = re.sub(r"\s+", " ", value).strip()
        if len(normalized) < 2 or len(normalized) > 100:
            raise InvalidLocationException("City must have 2 to 100 characters.")

        object.__setattr__(self, "_value", normalized)
        super().__init__()

    @property
    def value(self) -> str:
        """Return the normalized city."""
        return self._value

    @property
    def equality_components(self) -> tuple[Hashable, ...]:
        """Return values that define equality."""
        return (self._value.casefold(),)

    def __str__(self) -> str:
        return self._value
