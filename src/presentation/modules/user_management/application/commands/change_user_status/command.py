from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ChangeUserActiveStatusCommand:
    """Command that requests a user active status change."""

    actor_user_id: str
    target_user_id: str
    is_active: bool
