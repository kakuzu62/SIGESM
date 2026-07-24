from __future__ import annotations

from presentation.modules.user_management.application.commands.assign_user_roles.command import (
    AssignUserRolesCommand,
)
from shared.kernel.identity import Identity
from shared.kernel.result import Result


class AssignUserRolesCommandValidator:
    """Validates assign user roles commands."""

    def validate(self, command: AssignUserRolesCommand) -> Result[AssignUserRolesCommand]:
        """Validate identifiers and role id uniqueness."""
        if not command.actor_user_id.strip():
            return Result.failure("Usuario autenticado e obrigatorio.")
        if not command.target_user_id.strip():
            return Result.failure("Usuario alvo e obrigatorio.")

        try:
            Identity.from_string(command.actor_user_id.strip())
            Identity.from_string(command.target_user_id.strip())
            role_ids = tuple(role_id.strip() for role_id in command.role_ids)
            for role_id in role_ids:
                Identity.from_string(role_id)
        except ValueError:
            return Result.failure("Identificador invalido.")

        if len(set(role_ids)) != len(role_ids):
            return Result.failure("Perfil duplicado na solicitacao.")

        return Result.success(
            AssignUserRolesCommand(
                actor_user_id=command.actor_user_id.strip(),
                target_user_id=command.target_user_id.strip(),
                role_ids=role_ids,
            )
        )
