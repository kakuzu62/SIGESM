from __future__ import annotations

from abc import ABC
from typing import Generic, TypeVar, final

IdentityT = TypeVar("IdentityT")


class Entity(ABC, Generic[IdentityT]):
    """Base class for domain entities identified by immutable identity."""

    __slots__ = ("_id",)
    _id: IdentityT

    def __init__(self, entity_id: IdentityT) -> None:
        object.__setattr__(self, "_id", entity_id)

    @property
    @final
    def id(self) -> IdentityT:
        """Return the immutable entity identity."""
        return self._id

    def __setattr__(self, name: str, value: object) -> None:
        if name == "_id" and hasattr(self, "_id"):
            raise AttributeError("Entity id is immutable after creation.")

        object.__setattr__(self, name, value)

    def __eq__(self, other: object) -> bool:
        if other is self:
            return True

        if not isinstance(other, Entity):
            return False

        return type(self) is type(other) and self.id == other.id

    def __hash__(self) -> int:
        return hash((type(self), self.id))
