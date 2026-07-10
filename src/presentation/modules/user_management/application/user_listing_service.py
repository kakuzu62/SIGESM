from __future__ import annotations

from presentation.modules.user_management.application.common import PagedResult
from presentation.modules.user_management.application.queries.list_users import (
    ListUsersHandler,
    ListUsersQuery,
    UserListItemDTO,
)
from presentation.modules.user_management.application.queries.search_users import (
    SearchUsersHandler,
    SearchUsersQuery,
)
from presentation.modules.user_management.domain.repositories import IUserListingRepository
from shared.kernel.result import Result


class UserListingService:
    """Application facade for user listing presentation."""

    def __init__(self, repository: IUserListingRepository) -> None:
        self._list_users = ListUsersHandler(repository)
        self._search_users = SearchUsersHandler(self._list_users)

    def list_users(self, query: ListUsersQuery) -> Result[PagedResult[UserListItemDTO]]:
        """List users."""
        return self._list_users.handle(query)

    def search_users(self, query: SearchUsersQuery) -> Result[PagedResult[UserListItemDTO]]:
        """Search users."""
        return self._search_users.handle(query)
