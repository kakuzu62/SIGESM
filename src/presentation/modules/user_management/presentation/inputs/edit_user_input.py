from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class EditUserInput:
    """Input model containing user editing form values."""

    user_id: str
    full_name: str
    username: str
    email: str
