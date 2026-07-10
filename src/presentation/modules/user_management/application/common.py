from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Generic, TypeVar

T = TypeVar("T")


class SortDirection(StrEnum):
    """Sort direction for listing queries."""

    ASC = "ASC"
    DESC = "DESC"


@dataclass(frozen=True, slots=True)
class PagedResult(Generic[T]):
    """Paged application result."""

    items: tuple[T, ...]
    total: int
    page: int
    page_size: int

    @property
    def total_pages(self) -> int:
        """Return the total number of pages."""
        if self.total == 0:
            return 1
        return ((self.total - 1) // self.page_size) + 1
