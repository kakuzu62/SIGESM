from __future__ import annotations

from domain.contracts.repository import IRepository, EntityIdT, EntityT


class BaseRepository(IRepository[EntityT, EntityIdT]):
    """Base domain repository contract for concrete persistence adapters."""
