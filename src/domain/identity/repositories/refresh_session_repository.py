from __future__ import annotations

from abc import abstractmethod

from domain.contracts.repository import IRepository
from domain.identity.entities import RefreshSession
from shared.kernel.identity import Identity


class IRefreshSessionRepository(IRepository[RefreshSession, Identity]):
    """Repository contract for refresh sessions."""

    @abstractmethod
    def get_by_token_hash(self, token_hash: str) -> RefreshSession | None:
        """Return a refresh session by token hash."""
        raise NotImplementedError
