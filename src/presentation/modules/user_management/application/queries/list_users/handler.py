from __future__ import annotations

from presentation.modules.user_management.application.common import PagedResult
from presentation.modules.user_management.application.queries.list_users.dto import (
    UserListItemDTO,
)
from presentation.modules.user_management.application.queries.list_users.query import (
    ListUsersQuery,
)
from presentation.modules.user_management.application.queries.list_users.validator import (
    ListUsersValidator,
)
from presentation.modules.user_management.domain.repositories import IUserListingRepository
from shared.kernel.result import Result


class ListUsersHandler:
    """Handles user listing queries."""

    def __init__(
        self,
        repository: IUserListingRepository,
        validator: ListUsersValidator | None = None,
    ) -> None:
        self._repository = repository
        self._validator = validator or ListUsersValidator()

    def handle(self, query: ListUsersQuery) -> Result[PagedResult[UserListItemDTO]]:
        """Return a paged list of users."""
        validation = self._validator.validate(query)
        if validation.is_failure:
            return Result.failure(validation.error)
        return Result.success(self._repository.list_users(query))
