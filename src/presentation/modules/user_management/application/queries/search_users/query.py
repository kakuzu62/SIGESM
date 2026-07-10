from __future__ import annotations

from dataclasses import dataclass

from presentation.modules.user_management.application.common import SortDirection


@dataclass(frozen=True, slots=True)
class SearchUsersQuery:
    """Search users query."""

    term: str
    page: int = 1
    page_size: int = 20
    sort_by: str = "login"
    direction: SortDirection = SortDirection.ASC
