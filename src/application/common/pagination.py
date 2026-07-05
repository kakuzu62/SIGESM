from __future__ import annotations

from dataclasses import dataclass
from math import ceil
from typing import Generic, TypeVar

from core.exceptions.validation import ValidationException

T = TypeVar("T")


@dataclass(frozen=True, slots=True)
class Pagination:
    """Pagination request parameters."""

    page: int = 1
    page_size: int = 50

    def __post_init__(self) -> None:
        if self.page < 1:
            raise ValidationException("Page must be greater than zero.")

        if self.page_size < 1:
            raise ValidationException("Page size must be greater than zero.")

    @property
    def offset(self) -> int:
        """Return the SQL offset for this pagination request."""
        return (self.page - 1) * self.page_size


@dataclass(frozen=True, slots=True)
class PageResult(Generic[T]):
    """Paginated result returned by application queries."""

    items: tuple[T, ...]
    total_items: int
    page: int
    page_size: int

    @property
    def total_pages(self) -> int:
        """Return the number of pages for the result set."""
        if self.total_items == 0:
            return 0

        return ceil(self.total_items / self.page_size)

    @property
    def has_next(self) -> bool:
        """Return whether another page exists."""
        return self.page < self.total_pages

    @property
    def has_previous(self) -> bool:
        """Return whether a previous page exists."""
        return self.page > 1
