from __future__ import annotations

from abc import ABC, abstractmethod

from presentation.modules.user_management.application.common import PagedResult
from presentation.modules.user_management.application.queries.list_users.dto import UserListItemDTO
from presentation.modules.user_management.application.queries.list_users.query import ListUsersQuery


class IUserListingRepository(ABC):
    """Read repository contract for user listing."""

    @abstractmethod
    def list_users(self, query: ListUsersQuery) -> PagedResult[UserListItemDTO]:
        """Return a paged user list."""
        raise NotImplementedError

    @abstractmethod
    def search(self, query: ListUsersQuery) -> PagedResult[UserListItemDTO]:
        """Search users."""
        raise NotImplementedError

    @abstractmethod
    def paginate(self, query: ListUsersQuery) -> PagedResult[UserListItemDTO]:
        """Paginate users."""
        raise NotImplementedError

    @abstractmethod
    def order(self, query: ListUsersQuery) -> PagedResult[UserListItemDTO]:
        """Order users."""
        raise NotImplementedError

    @abstractmethod
    def total(self, query: ListUsersQuery) -> int:
        """Return total rows for a query."""
        raise NotImplementedError
