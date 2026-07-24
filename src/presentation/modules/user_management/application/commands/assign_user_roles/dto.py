from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from domain.identity.entities import User


@dataclass(frozen=True, slots=True)
class AssignUserRolesResultDTO:
    """Safe DTO returned after assigning roles to a user."""

    id: str
    full_name: str
    username: str
    email: str
    active: bool
    roles: tuple[str, ...]
    role_ids: tuple[str, ...]
    updated_at: datetime

    @classmethod
    def from_domain(cls, user: User) -> AssignUserRolesResultDTO:
        """Create a safe DTO from a user aggregate."""
        return cls(
            id=str(user.id),
            full_name=user.full_name,
            username=user.username.value,
            email=user.email.value,
            active=user.active,
            roles=tuple(role.name for role in user.roles),
            role_ids=tuple(str(role.id) for role in user.roles),
            updated_at=user.updated_at,
        )
