from __future__ import annotations

from presentation.modules.user_management.application.commands.update_user.command import (
    UpdateUserCommand,
)
from shared.kernel.identity import Identity
from shared.kernel.result import Result


class UpdateUserCommandValidator:
    """Validates update user command input before domain mutation."""

    _max_full_name_length = 120

    def validate(self, command: UpdateUserCommand) -> Result[UpdateUserCommand]:
        """Validate command fields and return normalized input."""
        full_name = " ".join(command.full_name.strip().split())
        username = command.username.strip()
        email = command.email.strip()

        try:
            Identity.from_string(command.user_id)
        except ValueError:
            return Result.failure("Usuario informado e invalido.")
        if not full_name:
            return Result.failure("Nome completo e obrigatorio.")
        if len(full_name) > self._max_full_name_length:
            return Result.failure("Nome completo deve conter no maximo 120 caracteres.")
        if not username:
            return Result.failure("Login e obrigatorio.")
        if not email:
            return Result.failure("E-mail e obrigatorio.")
        return Result.success(
            UpdateUserCommand(
                user_id=command.user_id,
                full_name=full_name,
                username=username,
                email=email,
            )
        )
