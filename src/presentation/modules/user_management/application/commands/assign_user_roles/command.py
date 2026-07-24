from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AssignUserRolesCommand:
    """Command that replaces a user's assigned roles."""

    actor_user_id: str
    target_user_id: str
    role_ids: tuple[str, ...]
