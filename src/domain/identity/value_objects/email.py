from __future__ import annotations

from collections.abc import Hashable
import re

from domain.identity.exceptions import InvalidEmailException
from shared.kernel.value_object import ValueObject


class Email(ValueObject):
    """Normalized email address."""

    __slots__ = ("_value",)
    _value: str

    def __init__(self, value: str) -> None:
        normalized = value.strip().lower()
        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", normalized):
            raise InvalidEmailException("Email address is not valid.")

        object.__setattr__(self, "_value", normalized)
        super().__init__()

    @property
    def value(self) -> str:
        """Return normalized email address."""
        return self._value

    @property
    def equality_components(self) -> tuple[Hashable, ...]:
        """Return values that define equality."""
        return (self._value,)

    def __str__(self) -> str:
        return self._value
