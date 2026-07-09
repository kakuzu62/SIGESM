from __future__ import annotations

from dataclasses import dataclass

from presentation.modules.user_management.application.dto.paging import UserSearchCriteria


@dataclass(frozen=True, slots=True)
class GetUserQuery:
    """Query to get one user."""

    user_id: str


@dataclass(frozen=True, slots=True)
class GetUsersQuery:
    """Query to list users."""

    criteria: UserSearchCriteria = UserSearchCriteria()


@dataclass(frozen=True, slots=True)
class SearchUsersQuery:
    """Query to search users."""

    criteria: UserSearchCriteria


@dataclass(frozen=True, slots=True)
class PagedUsersQuery:
    """Query to return paged users."""

    criteria: UserSearchCriteria


@dataclass(frozen=True, slots=True)
class ActiveUsersQuery:
    """Query to return active users."""

    criteria: UserSearchCriteria = UserSearchCriteria()


@dataclass(frozen=True, slots=True)
class InactiveUsersQuery:
    """Query to return inactive users."""

    criteria: UserSearchCriteria = UserSearchCriteria()
