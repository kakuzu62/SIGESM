from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class UserListItemDTO:
    """User row returned by listing queries."""

    id: str
    login: str
    name: str
    email: str
    status: str
    profiles: tuple[str, ...]
    last_access_at: datetime | None
    created_at: datetime
