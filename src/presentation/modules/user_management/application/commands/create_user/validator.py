from __future__ import annotations

from presentation.modules.user_management.application.commands.create_user.command import (
    CreateUserCommand,
)
from shared.kernel.result import Result


class CreateUserCommandValidator:
    """Validates create user command input before domain construction."""

    _max_full_name_length = 120

    def validate(self, command: CreateUserCommand) -> Result[CreateUserCommand]:
        """Validate command fields."""
        full_name = " ".join(command.full_name.strip().split())
        username = command.username.strip()
        email = command.email.strip()

        if not full_name:
            return Result.failure("Nome completo e obrigatorio.")
        if len(full_name) > self._max_full_name_length:
            return Result.failure("Nome completo deve conter no maximo 120 caracteres.")
        if not username:
            return Result.failure("Login e obrigatorio.")
        if not email:
            return Result.failure("E-mail e obrigatorio.")
        if not command.password:
            return Result.failure("Senha inicial e obrigatoria.")
        return Result.success(
            CreateUserCommand(
                full_name=full_name,
                username=username,
                email=email,
                password=command.password,
            )
        )
