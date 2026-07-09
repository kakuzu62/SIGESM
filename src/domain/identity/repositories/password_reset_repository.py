from __future__ import annotations

from abc import abstractmethod

from domain.contracts.repository import IRepository
from domain.identity.entities import PasswordResetRequest
from shared.kernel.identity import Identity


class IPasswordResetRequestRepository(IRepository[PasswordResetRequest, Identity]):
    """Repository contract for password reset requests."""

    @abstractmethod
    def get_by_token_hash(self, token_hash: str) -> PasswordResetRequest | None:
        """Return a password reset request by token hash."""
        raise NotImplementedError

    @abstractmethod
    def get_active_by_user(self, user_id: Identity) -> PasswordResetRequest | None:
        """Return the active password reset request for a user."""
        raise NotImplementedError
