from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CreateUserInput:
    """Input model containing user creation form values."""

    full_name: str
    username: str
    email: str
    password: str
    password_confirmation: str
