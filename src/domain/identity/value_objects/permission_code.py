from __future__ import annotations

from collections.abc import Hashable
import re

from domain.identity.exceptions import InvalidPermissionCodeException
from shared.kernel.value_object import ValueObject


class PermissionCode(ValueObject):
    """Stable permission code used by authorization policies."""

    __slots__ = ("_value",)
    _value: str

    def __init__(self, value: str) -> None:
        normalized = value.strip().upper().replace(":", ".")
        if not re.fullmatch(r"[A-Z][A-Z0-9_.-]{2,96}", normalized):
            raise InvalidPermissionCodeException("Permission code is not valid.")

        object.__setattr__(self, "_value", normalized)
        super().__init__()

    @property
    def value(self) -> str:
        """Return normalized permission code."""
        return self._value

    @property
    def equality_components(self) -> tuple[Hashable, ...]:
        """Return values that define equality."""
        return (self._value,)

    def __str__(self) -> str:
        return self._value
