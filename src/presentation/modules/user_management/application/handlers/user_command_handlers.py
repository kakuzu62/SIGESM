from __future__ import annotations

from datetime import datetime

from domain.identity.entities import User
from domain.identity.services import PasswordService
from domain.identity.value_objects import Email, Username
from presentation.modules.user_management.application.commands import (
    ActivateUserCommand,
    AssignRoleCommand,
    CreateUserCommand,
    DeactivateUserCommand,
    DeleteUserCommand,
    RemoveRoleCommand,
    ResetPasswordCommand,
    UpdateUserCommand,
)
from presentation.modules.user_management.application.dto import UserDTO
from presentation.modules.user_management.application.mappings import UserMapper
from presentation.modules.user_management.application.validators import UserCommandValidator
from presentation.modules.user_management.domain.repositories import IUserManagementRepository
from presentation.modules.user_management.domain.services import UserAuditService
from shared.kernel.identity import Identity
from shared.kernel.result import Result


class CreateUserHandler:
    """Handles user creation."""

    def __init__(
        self,
        repository: IUserManagementRepository,
        password_service: PasswordService,
        validator: UserCommandValidator,
        audit: UserAuditService,
    ) -> None:
        self._repository = repository
        self._password_service = password_service
        self._validator = validator
        self._audit = audit

    def handle(self, command: CreateUserCommand) -> Result[UserDTO]:
        """Create a user."""
        validation = self._validator.validate_create(command.payload)
        if validation.is_failure:
            return Result.failure(validation.error)
        if self._repository.get_by_username(command.payload.username) is not None:
            return Result.failure("Username already exists.")
        if self._repository.get_by_email(command.payload.email) is not None:
            return Result.failure("Email already exists.")

        user = User.create(
            Username(command.payload.username),
            Email(command.payload.email),
            self._password_service.hash_password(command.payload.password),
        )
        for role_id in command.payload.role_ids:
            role = self._repository.get_role(Identity.from_string(role_id))
            if role is not None:
                user.assign_role(role)
        self._repository.add_user(user)
        self._audit.record("user_created", str(user.id), command.actor_id)
        return Result.success(UserMapper.to_dto(user))


class UpdateUserHandler:
    """Handles user updates."""

    def __init__(
        self,
        repository: IUserManagementRepository,
        validator: UserCommandValidator,
        audit: UserAuditService,
    ) -> None:
        self._repository = repository
        self._validator = validator
        self._audit = audit

    def handle(self, command: UpdateUserCommand) -> Result[UserDTO]:
        """Update user profile data and roles."""
        validation = self._validator.validate_update(command.payload)
        if validation.is_failure:
            return Result.failure(validation.error)
        user = self._repository.get_user(Identity.from_string(command.payload.user_id))
        if user is None:
            return Result.failure("User was not found.")
        duplicate_username = self._repository.get_by_username(command.payload.username)
        if duplicate_username is not None and duplicate_username.id != user.id:
            return Result.failure("Username already exists.")
        duplicate_email = self._repository.get_by_email(command.payload.email)
        if duplicate_email is not None and duplicate_email.id != user.id:
            return Result.failure("Email already exists.")

        roles = tuple(
            role
            for role_id in command.payload.role_ids
            if (role := self._repository.get_role(Identity.from_string(role_id))) is not None
        )
        updated = User(
            entity_id=user.id,
            username=Username(command.payload.username),
            email=Email(command.payload.email),
            password_hash=user.password_hash,
            roles=roles,
            active=user.active,
            failed_login_attempts=user.failed_login_attempts,
            locked_until=user.locked_until,
            created_at=user.created_at,
            updated_at=datetime.now(user.updated_at.tzinfo),
        )
        self._repository.update_user(updated)
        self._audit.record("user_updated", str(updated.id), command.actor_id)
        return Result.success(UserMapper.to_dto(updated))


class ActivateUserHandler:
    """Handles user activation."""

    def __init__(self, repository: IUserManagementRepository, audit: UserAuditService) -> None:
        self._repository = repository
        self._audit = audit

    def handle(self, command: ActivateUserCommand) -> Result[UserDTO]:
        """Activate a user."""
        user = self._repository.get_user(Identity.from_string(command.user_id))
        if user is None:
            return Result.failure("User was not found.")
        user.activate()
        self._repository.update_user(user)
        self._audit.record("user_activated", str(user.id), command.actor_id)
        return Result.success(UserMapper.to_dto(user))


class DeactivateUserHandler:
    """Handles user deactivation."""

    def __init__(self, repository: IUserManagementRepository, audit: UserAuditService) -> None:
        self._repository = repository
        self._audit = audit

    def handle(self, command: DeactivateUserCommand) -> Result[UserDTO]:
        """Deactivate a user."""
        if command.actor_id == command.user_id:
            return Result.failure("The current user cannot deactivate itself.")
        user = self._repository.get_user(Identity.from_string(command.user_id))
        if user is None:
            return Result.failure("User was not found.")
        if _is_admin(user) and self._repository.count_active_admins() <= 1:
            return Result.failure("The last administrator cannot be deactivated.")
        try:
            user.deactivate(command.reason)
        except Exception as exc:
            return Result.failure(str(exc))
        self._repository.update_user(user)
        self._audit.record("user_deactivated", str(user.id), command.actor_id)
        return Result.success(UserMapper.to_dto(user))


class ResetPasswordHandler:
    """Handles password reset."""

    def __init__(
        self,
        repository: IUserManagementRepository,
        password_service: PasswordService,
        validator: UserCommandValidator,
        audit: UserAuditService,
    ) -> None:
        self._repository = repository
        self._password_service = password_service
        self._validator = validator
        self._audit = audit

    def handle(self, command: ResetPasswordCommand) -> Result[UserDTO]:
        """Reset a user password."""
        validation = self._validator.validate_password(command.new_password)
        if validation.is_failure:
            return Result.failure(validation.error)
        user = self._repository.get_user(Identity.from_string(command.user_id))
        if user is None:
            return Result.failure("User was not found.")
        user.change_password(self._password_service.hash_password(command.new_password))
        self._repository.update_user(user)
        self._audit.record("password_reset", str(user.id), command.actor_id)
        return Result.success(UserMapper.to_dto(user))


class AssignRoleHandler:
    """Handles role assignment."""

    def __init__(self, repository: IUserManagementRepository, audit: UserAuditService) -> None:
        self._repository = repository
        self._audit = audit

    def handle(self, command: AssignRoleCommand) -> Result[UserDTO]:
        """Assign a role to a user."""
        user = self._repository.get_user(Identity.from_string(command.user_id))
        role = self._repository.get_role(Identity.from_string(command.role_id))
        if user is None or role is None:
            return Result.failure("User or role was not found.")
        user.assign_role(role)
        self._repository.update_user(user)
        self._audit.record("role_assigned", str(user.id), command.actor_id)
        return Result.success(UserMapper.to_dto(user))


class RemoveRoleHandler:
    """Handles role removal."""

    def __init__(self, repository: IUserManagementRepository, audit: UserAuditService) -> None:
        self._repository = repository
        self._audit = audit

    def handle(self, command: RemoveRoleCommand) -> Result[UserDTO]:
        """Remove a role from a user."""
        user = self._repository.get_user(Identity.from_string(command.user_id))
        role = self._repository.get_role(Identity.from_string(command.role_id))
        if user is None or role is None:
            return Result.failure("User or role was not found.")
        if (
            _is_admin(user)
            and role.name.lower() == "admin"
            and self._repository.count_active_admins() <= 1
        ):
            return Result.failure("The last administrator role cannot be removed.")
        user.remove_role(role)
        self._repository.update_user(user)
        self._audit.record("role_removed", str(user.id), command.actor_id)
        return Result.success(UserMapper.to_dto(user))


class DeleteUserHandler:
    """Handles soft deletion."""

    def __init__(self, repository: IUserManagementRepository, audit: UserAuditService) -> None:
        self._repository = repository
        self._audit = audit

    def handle(self, command: DeleteUserCommand) -> Result[UserDTO]:
        """Soft delete a user by deactivating it."""
        return DeactivateUserHandler(self._repository, self._audit).handle(
            DeactivateUserCommand(
                user_id=command.user_id,
                reason="Soft delete requested.",
                actor_id=command.actor_id,
            )
        )


def _is_admin(user: User) -> bool:
    return any(role.name.lower() == "admin" for role in user.roles)
