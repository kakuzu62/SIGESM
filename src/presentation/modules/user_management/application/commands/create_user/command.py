from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CreateUserCommand:
    """Command containing the data required to create a user."""

    full_name: str
    username: str
    email: str
    password: str
