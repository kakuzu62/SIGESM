from __future__ import annotations

from collections.abc import Hashable

from domain.identity.exceptions import InvalidPasswordHashException
from shared.kernel.value_object import ValueObject


class PasswordHash(ValueObject):
    """Encoded password hash value object."""

    __slots__ = ("_value",)
    _value: str

    def __init__(self, value: str) -> None:
        normalized = value.strip()
        parts = normalized.split("$")
        if len(parts) != 4 or parts[0] != "pbkdf2_sha256":
            raise InvalidPasswordHashException("Password hash format is not supported.")

        object.__setattr__(self, "_value", normalized)
        super().__init__()

    @property
    def value(self) -> str:
        """Return encoded password hash."""
        return self._value

    @property
    def equality_components(self) -> tuple[Hashable, ...]:
        """Return values that define equality."""
        return (self._value,)

    def __str__(self) -> str:
        return self._value
