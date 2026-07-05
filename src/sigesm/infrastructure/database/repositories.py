from __future__ import annotations

from typing import Generic, TypeVar

from sqlalchemy.orm import Session

EntityT = TypeVar("EntityT")
EntityIdT = TypeVar("EntityIdT")


class SqlAlchemyRepository(Generic[EntityT, EntityIdT]):
    entity_type: type[EntityT]

    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, entity: EntityT) -> None:
        self._session.add(entity)

    def get(self, entity_id: EntityIdT) -> EntityT | None:
        return self._session.get(self.entity_type, entity_id)
