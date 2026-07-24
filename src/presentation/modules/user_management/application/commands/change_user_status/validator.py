from __future__ import annotations

from presentation.modules.user_management.application.commands.change_user_status.command import (
    ChangeUserActiveStatusCommand,
)
from shared.kernel.identity import Identity
from shared.kernel.result import Result


class ChangeUserActiveStatusCommandValidator:
    """Validates active status command input."""

    def validate(
        self, command: ChangeUserActiveStatusCommand
    ) -> Result[ChangeUserActiveStatusCommand]:
        """Validate command identifiers and return the command when valid."""
        if not command.actor_user_id.strip():
            return Result.failure("Usuario autenticado e obrigatorio.")
        if not command.target_user_id.strip():
            return Result.failure("Usuario alvo e obrigatorio.")

        try:
            Identity.from_string(command.actor_user_id.strip())
            Identity.from_string(command.target_user_id.strip())
        except ValueError:
            return Result.failure("Identificador de usuario invalido.")

        return Result.success(
            ChangeUserActiveStatusCommand(
                actor_user_id=command.actor_user_id.strip(),
                target_user_id=command.target_user_id.strip(),
                is_active=command.is_active,
            )
        )
