from __future__ import annotations

from abc import abstractmethod

from domain.contracts.repository import IRepository
from domain.identity.entities import AuthenticationSession
from shared.kernel.identity import Identity


class IAuthenticationSessionRepository(IRepository[AuthenticationSession, Identity]):
    """Repository contract for authentication sessions."""

    @abstractmethod
    def get_by_token_hash(self, token_hash: str) -> AuthenticationSession | None:
        """Return an authentication session by token hash."""
        raise NotImplementedError

    @abstractmethod
    def list_active_by_user(self, user_id: Identity) -> tuple[AuthenticationSession, ...]:
        """Return active sessions for a user."""
        raise NotImplementedError
