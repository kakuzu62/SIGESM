from __future__ import annotations

from dataclasses import dataclass

from presentation.modules.user_management.application.common import SortDirection


@dataclass(frozen=True, slots=True)
class ListUsersQuery:
    """Query for paged user listing."""

    page: int = 1
    page_size: int = 20
    sort_by: str = "login"
    direction: SortDirection = SortDirection.ASC
    filter_text: str = ""
