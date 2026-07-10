from __future__ import annotations

from presentation.modules.user_management.application.queries.list_users.query import ListUsersQuery
from shared.kernel.result import Result


class ListUsersValidator:
    """Validates list users query parameters."""

    _allowed_sort_fields = {"login", "name", "email", "status", "last_access_at", "created_at"}

    def validate(self, query: ListUsersQuery) -> Result[ListUsersQuery]:
        """Validate query parameters."""
        if query.page < 1:
            return Result.failure("Page must be greater than zero.")
        if query.page_size < 1 or query.page_size > 100:
            return Result.failure("Page size must be between 1 and 100.")
        if query.sort_by not in self._allowed_sort_fields:
            return Result.failure("Sort field is not supported.")
        return Result.success(query)
