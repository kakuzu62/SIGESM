from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Generic, TypeVar


class UserStatusFilter(StrEnum):
    """Status filter for user searches."""

    ALL = "ALL"
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


class SortDirection(StrEnum):
    """Sort direction for user searches."""

    ASC = "ASC"
    DESC = "DESC"


@dataclass(frozen=True, slots=True)
class UserSearchCriteria:
    """Search criteria for users."""

    term: str = ""
    status: UserStatusFilter = UserStatusFilter.ALL
    page: int = 1
    page_size: int = 20
    sort_by: str = "username"
    direction: SortDirection = SortDirection.ASC


T = TypeVar("T")


@dataclass(frozen=True, slots=True)
class Page(Generic[T]):
    """Paged result."""

    items: tuple[T, ...]
    total: int
    page: int
    page_size: int

    @property
    def total_pages(self) -> int:
        """Return total number of pages."""
        if self.total == 0:
            return 1
        return ((self.total - 1) // self.page_size) + 1
