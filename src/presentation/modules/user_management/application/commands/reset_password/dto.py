from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from domain.identity.entities import User


@dataclass(frozen=True, slots=True)
class ResetPasswordResultDTO:
    """Safe DTO returned after an administrator password reset."""

    id: str
    full_name: str
    username: str
    email: str
    active: bool
    updated_at: datetime

    @classmethod
    def from_domain(cls, user: User) -> ResetPasswordResultDTO:
        """Create a safe DTO from a user aggregate."""
        return cls(
            id=str(user.id),
            full_name=user.full_name,
            username=user.username.value,
            email=user.email.value,
            active=user.active,
            updated_at=user.updated_at,
        )
