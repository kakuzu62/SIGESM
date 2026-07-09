from __future__ import annotations

from dataclasses import dataclass

from presentation.modules.user_management.application.dto import CreateUserDTO, UpdateUserDTO


@dataclass(frozen=True, slots=True)
class CreateUserCommand:
    """Command to create a user."""

    payload: CreateUserDTO
    actor_id: str | None = None


@dataclass(frozen=True, slots=True)
class UpdateUserCommand:
    """Command to update a user."""

    payload: UpdateUserDTO
    actor_id: str | None = None


@dataclass(frozen=True, slots=True)
class ActivateUserCommand:
    """Command to activate a user."""

    user_id: str
    actor_id: str | None = None


@dataclass(frozen=True, slots=True)
class DeactivateUserCommand:
    """Command to deactivate a user."""

    user_id: str
    reason: str
    actor_id: str | None = None


@dataclass(frozen=True, slots=True)
class ResetPasswordCommand:
    """Command to reset a user password."""

    user_id: str
    new_password: str
    actor_id: str | None = None


@dataclass(frozen=True, slots=True)
class AssignRoleCommand:
    """Command to assign a role to a user."""

    user_id: str
    role_id: str
    actor_id: str | None = None


@dataclass(frozen=True, slots=True)
class RemoveRoleCommand:
    """Command to remove a role from a user."""

    user_id: str
    role_id: str
    actor_id: str | None = None


@dataclass(frozen=True, slots=True)
class DeleteUserCommand:
    """Command to soft delete a user."""

    user_id: str
    actor_id: str | None = None
