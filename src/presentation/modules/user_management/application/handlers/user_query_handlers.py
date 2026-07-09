from __future__ import annotations

from presentation.modules.user_management.application.dto import UserDetailsDTO, UserListItemDTO
from presentation.modules.user_management.application.dto.paging import (
    Page,
    UserSearchCriteria,
    UserStatusFilter,
)
from presentation.modules.user_management.application.mappings import UserMapper
from presentation.modules.user_management.application.queries import (
    ActiveUsersQuery,
    GetUserQuery,
    GetUsersQuery,
    InactiveUsersQuery,
    PagedUsersQuery,
    SearchUsersQuery,
)
from presentation.modules.user_management.domain.repositories import IUserManagementRepository
from shared.kernel.identity import Identity
from shared.kernel.result import Result


class GetUserHandler:
    """Handles get user query."""

    def __init__(self, repository: IUserManagementRepository) -> None:
        self._repository = repository

    def handle(self, query: GetUserQuery) -> Result[UserDetailsDTO]:
        """Return a user by id."""
        user = self._repository.get_user(Identity.from_string(query.user_id))
        if user is None:
            return Result.failure("User was not found.")
        return Result.success(UserMapper.to_details(user))


class SearchUsersHandler:
    """Handles search users query."""

    def __init__(self, repository: IUserManagementRepository) -> None:
        self._repository = repository

    def handle(self, query: SearchUsersQuery) -> Result[Page[UserListItemDTO]]:
        """Search users."""
        page = self._repository.search_users(query.criteria)
        return Result.success(
            Page(
                items=tuple(UserMapper.to_list_item(user) for user in page.items),
                total=page.total,
                page=page.page,
                page_size=page.page_size,
            )
        )


class PagedUsersHandler:
    """Handles paged user query."""

    def __init__(self, repository: IUserManagementRepository) -> None:
        self._search = SearchUsersHandler(repository)

    def handle(self, query: PagedUsersQuery) -> Result[Page[UserListItemDTO]]:
        """Return paged users."""
        return self._search.handle(SearchUsersQuery(query.criteria))


class GetUsersHandler:
    """Handles list users query."""

    def __init__(self, repository: IUserManagementRepository) -> None:
        self._search = SearchUsersHandler(repository)

    def handle(self, query: GetUsersQuery) -> Result[Page[UserListItemDTO]]:
        """Return users."""
        return self._search.handle(SearchUsersQuery(query.criteria))


class ActiveUsersHandler:
    """Handles active users query."""

    def __init__(self, repository: IUserManagementRepository) -> None:
        self._search = SearchUsersHandler(repository)

    def handle(self, query: ActiveUsersQuery) -> Result[Page[UserListItemDTO]]:
        """Return active users."""
        criteria = UserSearchCriteria(
            term=query.criteria.term,
            status=UserStatusFilter.ACTIVE,
            page=query.criteria.page,
            page_size=query.criteria.page_size,
            sort_by=query.criteria.sort_by,
            direction=query.criteria.direction,
        )
        return self._search.handle(SearchUsersQuery(criteria))


class InactiveUsersHandler:
    """Handles inactive users query."""

    def __init__(self, repository: IUserManagementRepository) -> None:
        self._search = SearchUsersHandler(repository)

    def handle(self, query: InactiveUsersQuery) -> Result[Page[UserListItemDTO]]:
        """Return inactive users."""
        criteria = UserSearchCriteria(
            term=query.criteria.term,
            status=UserStatusFilter.INACTIVE,
            page=query.criteria.page,
            page_size=query.criteria.page_size,
            sort_by=query.criteria.sort_by,
            direction=query.criteria.direction,
        )
        return self._search.handle(SearchUsersQuery(criteria))
