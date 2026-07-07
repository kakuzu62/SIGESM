from __future__ import annotations

from abc import abstractmethod

from domain.contracts.repository import IRepository
from domain.identity.entities import User
from domain.identity.value_objects import Email, Username
from shared.kernel.identity import Identity


class IUserRepository(IRepository[User, Identity]):
    """Repository contract for users."""

    @abstractmethod
    def get_by_username(self, username: Username) -> User | None:
        """Return a user by username."""
        raise NotImplementedError

    @abstractmethod
    def get_by_email(self, email: Email) -> User | None:
        """Return a user by email."""
        raise NotImplementedError
