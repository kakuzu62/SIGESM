from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class RoleDTO:
    """Role option available to user management."""

    id: str
    name: str
    description: str


@dataclass(frozen=True, slots=True)
class UserDTO:
    """User data transfer object."""

    id: str
    username: str
    email: str
    active: bool
    roles: tuple[RoleDTO, ...]
    created_at: datetime
    updated_at: datetime


@dataclass(frozen=True, slots=True)
class CreateUserDTO:
    """Data required to create a user."""

    username: str
    email: str
    password: str
    role_ids: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class UpdateUserDTO:
    """Data required to update a user."""

    user_id: str
    username: str
    email: str
    role_ids: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class UserListItemDTO:
    """Compact user DTO for tables."""

    id: str
    username: str
    email: str
    active: bool
    roles: tuple[str, ...]
    updated_at: datetime


@dataclass(frozen=True, slots=True)
class UserDetailsDTO(UserDTO):
    """Detailed user DTO."""
