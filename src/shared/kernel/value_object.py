from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Hashable


class ValueObject(ABC):
    """Immutable object whose equality is based on component values."""

    __slots__ = ("_is_frozen",)

    def __init__(self) -> None:
        object.__setattr__(self, "_is_frozen", True)

    @property
    @abstractmethod
    def equality_components(self) -> tuple[Hashable, ...]:
        """Return values that define equality for this object."""
        raise NotImplementedError

    def __setattr__(self, name: str, value: object) -> None:
        if getattr(self, "_is_frozen", False):
            raise AttributeError(f"{type(self).__name__} is immutable.")

        object.__setattr__(self, name, value)

    def __eq__(self, other: object) -> bool:
        if other is self:
            return True

        if type(self) is not type(other):
            return False

        return self.equality_components == other.equality_components

    def __hash__(self) -> int:
        return hash((type(self), self.equality_components))
