from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import Generic, TypeVar

EntityT = TypeVar("EntityT")
EntityIdT = TypeVar("EntityIdT")


class IRepository(ABC, Generic[EntityT, EntityIdT]):
    """Domain repository contract for aggregate persistence."""

    @abstractmethod
    def add(self, entity: EntityT) -> EntityT:
        """Add an entity to the current persistence context."""
        raise NotImplementedError

    @abstractmethod
    def update(self, entity: EntityT) -> EntityT:
        """Update an entity in the current persistence context."""
        raise NotImplementedError

    @abstractmethod
    def delete(self, entity: EntityT) -> None:
        """Delete an entity from the current persistence context."""
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, entity_id: EntityIdT) -> EntityT | None:
        """Return an entity by identity."""
        raise NotImplementedError

    @abstractmethod
    def exists(self, entity_id: EntityIdT) -> bool:
        """Return whether an entity exists for the given identity."""
        raise NotImplementedError

    @abstractmethod
    def count(self) -> int:
        """Return the total number of persisted entities."""
        raise NotImplementedError

    @abstractmethod
    def list(self) -> Sequence[EntityT]:
        """Return persisted entities."""
        raise NotImplementedError

    @abstractmethod
    def first(self) -> EntityT | None:
        """Return the first persisted entity."""
        raise NotImplementedError
