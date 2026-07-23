from __future__ import annotations

from core.exceptions.validation import ValidationException
from domain.identity.exceptions import IdentityDomainException, InvalidEmailException
from domain.identity.exceptions import InvalidUsernameException
from domain.identity.value_objects import Email, Username
from presentation.modules.user_management.application.commands.update_user.command import (
    UpdateUserCommand,
)
from presentation.modules.user_management.application.commands.update_user.dto import (
    UpdateUserResultDTO,
)
from presentation.modules.user_management.application.commands.update_user.unit_of_work import (
    UserUpdateConflictError,
    UserUpdateUnitOfWorkFactory,
)
from presentation.modules.user_management.application.commands.update_user.validator import (
    UpdateUserCommandValidator,
)
from shared.kernel.identity import Identity
from shared.kernel.result import Result


class UpdateUserHandler:
    """Handles the update user command."""

    def __init__(
        self,
        unit_of_work_factory: UserUpdateUnitOfWorkFactory,
        validator: UpdateUserCommandValidator | None = None,
    ) -> None:
        self._unit_of_work_factory = unit_of_work_factory
        self._validator = validator or UpdateUserCommandValidator()

    def handle(self, command: UpdateUserCommand) -> Result[UpdateUserResultDTO]:
        """Update a user profile and return a safe DTO."""
        validation = self._validator.validate(command)
        if validation.is_failure:
            return Result.failure(validation.error)

        normalized = validation.value
        user_id = Identity.from_string(normalized.user_id)
        try:
            username = Username(normalized.username)
            email = Email(normalized.email)
        except InvalidUsernameException:
            return Result.failure("Login informado e invalido.")
        except InvalidEmailException:
            return Result.failure("E-mail informado e invalido.")

        with self._unit_of_work_factory.create() as unit_of_work:
            user = unit_of_work.users.get_by_id(user_id)
            if user is None:
                unit_of_work.rollback()
                return Result.failure("Usuario nao encontrado.")

            user_with_username = unit_of_work.users.get_by_username(username)
            if user_with_username is not None and user_with_username.id != user_id:
                unit_of_work.rollback()
                return Result.failure("Este login ja esta em uso.")

            user_with_email = unit_of_work.users.get_by_email(email)
            if user_with_email is not None and user_with_email.id != user_id:
                unit_of_work.rollback()
                return Result.failure("Este e-mail ja esta em uso.")

            try:
                user.update_profile(normalized.full_name, username, email)
                unit_of_work.users.update(user)
                unit_of_work.commit()
            except UserUpdateConflictError:
                unit_of_work.rollback()
                return Result.failure("Este login ou e-mail ja esta em uso.")
            except (IdentityDomainException, ValidationException) as exc:
                unit_of_work.rollback()
                return Result.failure(str(exc))

        return Result.success(UpdateUserResultDTO.from_domain(user))
