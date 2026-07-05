from __future__ import annotations

from abc import ABC
from typing import Generic, TypeVar

from sqlalchemy.orm import Session

EntityT = TypeVar("EntityT")
EntityIdT = TypeVar("EntityIdT")


class SqlAlchemyRepository(ABC, Generic[EntityT, EntityIdT]):
    """Base repository with common SQLAlchemy persistence operations."""

    entity_type: type[EntityT]

    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, entity: EntityT) -> None:
        """Persist a new entity instance in the current session."""
        self._session.add(entity)

    def get(self, entity_id: EntityIdT) -> EntityT | None:
        """Return an entity by identifier or None when it does not exist."""
        return self._session.get(self.entity_type, entity_id)

    def delete(self, entity: EntityT) -> None:
        """Delete an entity instance from the current session."""
        self._session.delete(entity)
