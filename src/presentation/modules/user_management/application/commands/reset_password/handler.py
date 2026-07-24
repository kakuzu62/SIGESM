from __future__ import annotations

from core.exceptions.validation import ValidationException
from domain.identity.exceptions import IdentityDomainException
from domain.identity.services import PasswordService
from presentation.modules.user_management.application.commands.reset_password.command import (
    ResetPasswordCommand,
)
from presentation.modules.user_management.application.commands.reset_password.dto import (
    ResetPasswordResultDTO,
)
from presentation.modules.user_management.application.commands.reset_password.unit_of_work import (
    PasswordResetPersistenceError,
    ResetPasswordUnitOfWorkFactory,
)
from presentation.modules.user_management.application.commands.reset_password.validator import (
    ResetPasswordCommandValidator,
)
from shared.kernel.identity import Identity
from shared.kernel.result import Result


class ResetPasswordHandler:
    """Handles administrator password reset."""

    def __init__(
        self,
        unit_of_work_factory: ResetPasswordUnitOfWorkFactory,
        password_service: PasswordService,
        validator: ResetPasswordCommandValidator | None = None,
    ) -> None:
        self._unit_of_work_factory = unit_of_work_factory
        self._password_service = password_service
        self._validator = validator or ResetPasswordCommandValidator()

    def handle(self, command: ResetPasswordCommand) -> Result[ResetPasswordResultDTO]:
        """Reset a user's password using the configured PasswordService."""
        validation = self._validator.validate(command)
        if validation.is_failure:
            return Result.failure(validation.error)

        normalized = validation.value
        target_id = Identity.from_string(normalized.target_user_id)

        with self._unit_of_work_factory.create() as unit_of_work:
            user = unit_of_work.users.get_by_id(target_id)
            if user is None:
                unit_of_work.rollback()
                return Result.failure("Usuario nao encontrado.")

            try:
                password_hash = self._password_service.hash_password(normalized.new_password)
                user.change_password(password_hash)
                unit_of_work.users.update(user)
                unit_of_work.commit()
            except PasswordResetPersistenceError:
                unit_of_work.rollback()
                return Result.failure("Nao foi possivel redefinir a senha.")
            except (IdentityDomainException, ValidationException) as exc:
                unit_of_work.rollback()
                return Result.failure(str(exc))

        return Result.success(ResetPasswordResultDTO.from_domain(user))
