from __future__ import annotations

from presentation.modules.user_management.application.commands.reset_password.command import (
    ResetPasswordCommand,
)
from shared.kernel.identity import Identity
from shared.kernel.result import Result


class ResetPasswordCommandValidator:
    """Validates administrator password reset commands."""

    def validate(self, command: ResetPasswordCommand) -> Result[ResetPasswordCommand]:
        """Validate identifiers and required password input."""
        if not command.actor_user_id.strip():
            return Result.failure("Usuario autenticado e obrigatorio.")
        if not command.target_user_id.strip():
            return Result.failure("Usuario alvo e obrigatorio.")
        if not command.new_password:
            return Result.failure("Nova senha e obrigatoria.")

        try:
            Identity.from_string(command.actor_user_id.strip())
            Identity.from_string(command.target_user_id.strip())
        except ValueError:
            return Result.failure("Identificador de usuario invalido.")

        return Result.success(
            ResetPasswordCommand(
                actor_user_id=command.actor_user_id.strip(),
                target_user_id=command.target_user_id.strip(),
                new_password=command.new_password,
            )
        )
