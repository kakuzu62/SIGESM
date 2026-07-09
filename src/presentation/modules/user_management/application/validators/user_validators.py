from __future__ import annotations

from dataclasses import dataclass

from domain.identity.services import PasswordService
from domain.identity.value_objects import Email, Username
from presentation.modules.user_management.application.dto import CreateUserDTO, UpdateUserDTO
from shared.kernel.result import Result


@dataclass(frozen=True, slots=True)
class UserCommandValidator:
    """Validates user management input without raising for expected failures."""

    password_service: PasswordService

    def validate_create(self, dto: CreateUserDTO) -> Result[CreateUserDTO]:
        """Validate create user input."""
        try:
            Username(dto.username)
            Email(dto.email)
            self.password_service.hash_password(dto.password)
        except Exception as exc:
            return Result.failure(str(exc))
        return Result.success(dto)

    def validate_update(self, dto: UpdateUserDTO) -> Result[UpdateUserDTO]:
        """Validate update user input."""
        try:
            Username(dto.username)
            Email(dto.email)
        except Exception as exc:
            return Result.failure(str(exc))
        if not dto.user_id.strip():
            return Result.failure("User id is required.")
        return Result.success(dto)

    def validate_password(self, password: str) -> Result[str]:
        """Validate a raw password."""
        try:
            self.password_service.hash_password(password)
        except Exception as exc:
            return Result.failure(str(exc))
        return Result.success(password)
