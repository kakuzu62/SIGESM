from __future__ import annotations

from abc import ABC, abstractmethod

from domain.identity.entities import Role, User
from presentation.modules.user_management.application.dto.paging import Page, UserSearchCriteria
from shared.kernel.identity import Identity


class IUserManagementRepository(ABC):
    """Repository contract for user management use cases."""

    @abstractmethod
    def add_user(self, user: User) -> User:
        """Add a user."""
        raise NotImplementedError

    @abstractmethod
    def update_user(self, user: User) -> User:
        """Update a user."""
        raise NotImplementedError

    @abstractmethod
    def get_user(self, user_id: Identity) -> User | None:
        """Return a user by id."""
        raise NotImplementedError

    @abstractmethod
    def get_by_username(self, username: str) -> User | None:
        """Return a user by username."""
        raise NotImplementedError

    @abstractmethod
    def get_by_email(self, email: str) -> User | None:
        """Return a user by email."""
        raise NotImplementedError

    @abstractmethod
    def search_users(self, criteria: UserSearchCriteria) -> Page[User]:
        """Search users."""
        raise NotImplementedError

    @abstractmethod
    def count_active_admins(self) -> int:
        """Return active administrator count."""
        raise NotImplementedError

    @abstractmethod
    def get_role(self, role_id: Identity) -> Role | None:
        """Return a role by id."""
        raise NotImplementedError

    @abstractmethod
    def list_roles(self) -> tuple[Role, ...]:
        """Return available roles."""
        raise NotImplementedError
