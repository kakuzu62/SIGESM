from __future__ import annotations

from collections.abc import Hashable
import re

from domain.identity.exceptions import InvalidUsernameException
from shared.kernel.value_object import ValueObject


class Username(ValueObject):
    """Normalized username used for authentication."""

    __slots__ = ("_value",)
    _value: str

    def __init__(self, value: str) -> None:
        normalized = value.strip().lower()
        if not re.fullmatch(r"[a-z0-9_.-]{3,64}", normalized):
            raise InvalidUsernameException(
                "Username must contain 3 to 64 letters, numbers, dots, underscores or hyphens."
            )

        object.__setattr__(self, "_value", normalized)
        super().__init__()

    @property
    def value(self) -> str:
        """Return normalized username."""
        return self._value

    @property
    def equality_components(self) -> tuple[Hashable, ...]:
        """Return values that define equality."""
        return (self._value,)

    def __str__(self) -> str:
        return self._value
