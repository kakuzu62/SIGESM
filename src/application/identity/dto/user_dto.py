from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from domain.identity.entities import User


@dataclass(frozen=True, slots=True)
class UserDTO:
    """Application DTO representing a user."""

    id: str
    username: str
    email: str
    active: bool
    roles: tuple[str, ...]
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_domain(cls, user: User) -> UserDTO:
        """Create a DTO from a user aggregate."""
        return cls(
            id=str(user.id),
            username=user.username.value,
            email=user.email.value,
            active=user.active,
            roles=tuple(role.name for role in user.roles),
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
