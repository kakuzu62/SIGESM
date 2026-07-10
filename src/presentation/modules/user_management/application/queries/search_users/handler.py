from __future__ import annotations

from presentation.modules.user_management.application.common import PagedResult
from presentation.modules.user_management.application.queries.list_users import (
    ListUsersHandler,
    ListUsersQuery,
    UserListItemDTO,
)
from presentation.modules.user_management.application.queries.search_users.query import (
    SearchUsersQuery,
)
from shared.kernel.result import Result


class SearchUsersHandler:
    """Handles user search queries."""

    def __init__(self, list_users_handler: ListUsersHandler) -> None:
        self._list_users_handler = list_users_handler

    def handle(self, query: SearchUsersQuery) -> Result[PagedResult[UserListItemDTO]]:
        """Search users using the list users pipeline."""
        return self._list_users_handler.handle(
            ListUsersQuery(
                page=query.page,
                page_size=query.page_size,
                sort_by=query.sort_by,
                direction=query.direction,
                filter_text=query.term,
            )
        )
