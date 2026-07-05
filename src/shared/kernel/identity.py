from __future__ import annotations

from collections.abc import Hashable
from uuid import UUID, uuid4

from shared.kernel.value_object import ValueObject


class Identity(ValueObject):
    """UUID-backed value object used as domain identity."""

    __slots__ = ("_value",)
    _value: UUID

    def __init__(self, value: UUID) -> None:
        object.__setattr__(self, "_value", value)
        super().__init__()

    @classmethod
    def new(cls) -> Identity:
        """Create a new identity value."""
        return cls(uuid4())

    @classmethod
    def from_string(cls, value: str) -> Identity:
        """Create an identity from a UUID string."""
        return cls(UUID(value))

    @property
    def value(self) -> UUID:
        """Return the wrapped UUID value."""
        return self._value

    @property
    def equality_components(self) -> tuple[Hashable, ...]:
        """Return values that define identity equality."""
        return (self._value,)

    def __str__(self) -> str:
        return str(self._value)
