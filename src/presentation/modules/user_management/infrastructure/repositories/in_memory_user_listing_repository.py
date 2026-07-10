from __future__ import annotations

from collections.abc import Iterable

from domain.identity.entities import User
from domain.identity.repositories import IUserRepository
from presentation.modules.user_management.application.common import PagedResult, SortDirection
from presentation.modules.user_management.application.queries.list_users import (
    ListUsersQuery,
    UserListItemDTO,
)
from presentation.modules.user_management.domain.repositories import IUserListingRepository


class InMemoryUserListingRepository(IUserListingRepository):
    """In-memory user listing repository for desktop bootstrap and tests."""

    def __init__(self, users: IUserRepository) -> None:
        self._users = users

    def list_users(self, query: ListUsersQuery) -> PagedResult[UserListItemDTO]:
        """Return a paged user list."""
        return self.paginate(query)

    def search(self, query: ListUsersQuery) -> PagedResult[UserListItemDTO]:
        """Search users."""
        return self.paginate(query)

    def order(self, query: ListUsersQuery) -> PagedResult[UserListItemDTO]:
        """Order users."""
        return self.paginate(query)

    def paginate(self, query: ListUsersQuery) -> PagedResult[UserListItemDTO]:
        """Paginate users."""
        filtered = self._filtered(query)
        ordered = self._ordered(filtered, query)
        start = (query.page - 1) * query.page_size
        end = start + query.page_size
        return PagedResult(
            items=tuple(self._to_dto(user) for user in ordered[start:end]),
            total=len(ordered),
            page=query.page,
            page_size=query.page_size,
        )

    def total(self, query: ListUsersQuery) -> int:
        """Return total rows for a query."""
        return len(self._filtered(query))

    def _filtered(self, query: ListUsersQuery) -> list[User]:
        term = query.filter_text.strip().lower()
        users = list(self._users.list())
        if not term:
            return users
        return [
            user
            for user in users
            if term in user.username.value.lower()
            or term in user.email.value.lower()
            or any(term in role.name.lower() for role in user.roles)
        ]

    @staticmethod
    def _ordered(users: Iterable[User], query: ListUsersQuery) -> list[User]:
        reverse = query.direction == SortDirection.DESC
        if query.sort_by == "email":
            return sorted(users, key=lambda user: user.email.value.lower(), reverse=reverse)
        if query.sort_by == "status":
            return sorted(users, key=lambda user: user.active, reverse=reverse)
        if query.sort_by == "created_at":
            return sorted(users, key=lambda user: user.created_at, reverse=reverse)
        return sorted(users, key=lambda user: user.username.value.lower(), reverse=reverse)

    @staticmethod
    def _to_dto(user: User) -> UserListItemDTO:
        return UserListItemDTO(
            id=str(user.id),
            login=user.username.value,
            name=user.username.value,
            email=user.email.value,
            status="Ativo" if user.active else "Inativo",
            profiles=tuple(role.name for role in user.roles),
            last_access_at=None,
            created_at=user.created_at,
        )
