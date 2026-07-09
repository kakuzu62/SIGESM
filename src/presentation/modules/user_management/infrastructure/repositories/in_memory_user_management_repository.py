from __future__ import annotations

from collections.abc import Sequence

from domain.identity.entities import Role, User
from domain.identity.repositories import IRoleRepository, IUserRepository
from domain.identity.value_objects import Email, Username
from presentation.modules.user_management.application.dto.paging import (
    Page,
    SortDirection,
    UserSearchCriteria,
    UserStatusFilter,
)
from presentation.modules.user_management.domain.repositories import IUserManagementRepository
from shared.kernel.identity import Identity


class InMemoryUserManagementRepository(IUserManagementRepository):
    """User management repository backed by identity repositories."""

    def __init__(self, users: IUserRepository, roles: IRoleRepository) -> None:
        self._users = users
        self._roles = roles

    def add_user(self, user: User) -> User:
        """Add a user."""
        return self._users.add(user)

    def update_user(self, user: User) -> User:
        """Update a user."""
        return self._users.update(user)

    def get_user(self, user_id: Identity) -> User | None:
        """Return a user by id."""
        return self._users.get_by_id(user_id)

    def get_by_username(self, username: str) -> User | None:
        """Return a user by username."""
        return self._users.get_by_username(Username(username))

    def get_by_email(self, email: str) -> User | None:
        """Return a user by email."""
        return self._users.get_by_email(Email(email))

    def search_users(self, criteria: UserSearchCriteria) -> Page[User]:
        """Search users in memory."""
        users = list(self._users.list())
        filtered = self._filter(users, criteria)
        sorted_users = self._sort(filtered, criteria)
        start = max(criteria.page - 1, 0) * criteria.page_size
        end = start + criteria.page_size
        return Page(
            items=tuple(sorted_users[start:end]),
            total=len(sorted_users),
            page=criteria.page,
            page_size=criteria.page_size,
        )

    def count_active_admins(self) -> int:
        """Return active administrator count."""
        return sum(
            1
            for user in self._users.list()
            if user.active and any(role.name.lower() == "admin" for role in user.roles)
        )

    def get_role(self, role_id: Identity) -> Role | None:
        """Return a role by id."""
        return self._roles.get_by_id(role_id)

    def list_roles(self) -> tuple[Role, ...]:
        """Return available roles."""
        return tuple(self._roles.list())

    @staticmethod
    def _filter(users: Sequence[User], criteria: UserSearchCriteria) -> list[User]:
        term = criteria.term.strip().lower()
        result = []
        for user in users:
            if criteria.status == UserStatusFilter.ACTIVE and not user.active:
                continue
            if criteria.status == UserStatusFilter.INACTIVE and user.active:
                continue
            if (
                term
                and term not in user.username.value.lower()
                and term not in user.email.value.lower()
            ):
                continue
            result.append(user)
        return result

    @staticmethod
    def _sort(users: list[User], criteria: UserSearchCriteria) -> list[User]:
        reverse = criteria.direction == SortDirection.DESC
        if criteria.sort_by == "email":
            return sorted(users, key=lambda user: user.email.value.lower(), reverse=reverse)
        if criteria.sort_by == "updated_at":
            return sorted(users, key=lambda user: user.updated_at, reverse=reverse)
        return sorted(users, key=lambda user: user.username.value.lower(), reverse=reverse)
