from __future__ import annotations

from typing import Generic, Protocol, TypeVar

EntityT = TypeVar("EntityT")
EntityIdT = TypeVar("EntityIdT", contravariant=True)


class Repository(Protocol, Generic[EntityT, EntityIdT]):
    def add(self, entity: EntityT) -> None:
        raise NotImplementedError

    def get(self, entity_id: EntityIdT) -> EntityT | None:
        raise NotImplementedError
