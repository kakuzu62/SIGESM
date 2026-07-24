from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ResetPasswordCommand:
    """Command that requests an administrator password reset."""

    actor_user_id: str
    target_user_id: str
    new_password: str
