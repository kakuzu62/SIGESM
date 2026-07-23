from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from domain.identity.entities import User


@dataclass(frozen=True, slots=True)
class UpdateUserResultDTO:
    """Safe DTO returned after a user profile is updated."""

    id: str
    full_name: str
    username: str
    email: str
    active: bool
    roles: tuple[str, ...]
    last_access_at: datetime | None
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_domain(cls, user: User) -> UpdateUserResultDTO:
        """Create a safe DTO from a user aggregate."""
        return cls(
            id=str(user.id),
            full_name=user.full_name,
            username=user.username.value,
            email=user.email.value,
            active=user.active,
            roles=tuple(role.name for role in user.roles),
            last_access_at=None,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
