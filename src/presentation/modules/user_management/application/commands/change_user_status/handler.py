from __future__ import annotations

from domain.identity.exceptions import IdentityDomainException
from presentation.modules.user_management.application.commands.change_user_status.command import (
    ChangeUserActiveStatusCommand,
)
from presentation.modules.user_management.application.commands.change_user_status.dto import (
    ChangeUserActiveStatusResultDTO,
)
from presentation.modules.user_management.application.commands.change_user_status.unit_of_work import (
    UserStatusConflictError,
    UserStatusUnitOfWorkFactory,
)
from presentation.modules.user_management.application.commands.change_user_status.validator import (
    ChangeUserActiveStatusCommandValidator,
)
from shared.kernel.identity import Identity
from shared.kernel.result import Result


class ChangeUserActiveStatusHandler:
    """Handles user active status changes."""

    _DEACTIVATION_REASON = "Administrative deactivation."

    def __init__(
        self,
        unit_of_work_factory: UserStatusUnitOfWorkFactory,
        validator: ChangeUserActiveStatusCommandValidator | None = None,
    ) -> None:
        self._unit_of_work_factory = unit_of_work_factory
        self._validator = validator or ChangeUserActiveStatusCommandValidator()

    def handle(
        self, command: ChangeUserActiveStatusCommand
    ) -> Result[ChangeUserActiveStatusResultDTO]:
        """Change a user's active status and return a safe DTO."""
        validation = self._validator.validate(command)
        if validation.is_failure:
            return Result.failure(validation.error)

        normalized = validation.value
        actor_id = Identity.from_string(normalized.actor_user_id)
        target_id = Identity.from_string(normalized.target_user_id)

        with self._unit_of_work_factory.create() as unit_of_work:
            user = unit_of_work.users.get_by_id(target_id)
            if user is None:
                unit_of_work.rollback()
                return Result.failure("Usuario nao encontrado.")

            if actor_id == target_id and not normalized.is_active:
                unit_of_work.rollback()
                return Result.failure("Voce nao pode desativar a propria conta.")

            if user.active == normalized.is_active:
                unit_of_work.rollback()
                state = "ativo" if normalized.is_active else "inativo"
                return Result.failure(f"Usuario ja esta {state}.")

            try:
                if normalized.is_active:
                    user.activate()
                else:
                    user.deactivate(self._DEACTIVATION_REASON)
                unit_of_work.users.update(user)
                unit_of_work.commit()
            except UserStatusConflictError:
                unit_of_work.rollback()
                return Result.failure("Nao foi possivel alterar o status do usuario.")
            except IdentityDomainException as exc:
                unit_of_work.rollback()
                return Result.failure(str(exc))

        return Result.success(ChangeUserActiveStatusResultDTO.from_domain(user))
