from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class UpdateUserCommand:
    """Command containing editable user profile data."""

    user_id: str
    full_name: str
    username: str
    email: str
