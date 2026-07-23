from __future__ import annotations

from core.exceptions.validation import ValidationException
from domain.identity.entities import User
from domain.identity.exceptions import IdentityDomainException, InvalidEmailException
from domain.identity.exceptions import InvalidPasswordException, InvalidUsernameException
from domain.identity.services import PasswordService
from domain.identity.value_objects import Email, Username
from presentation.modules.user_management.application.commands.create_user.command import (
    CreateUserCommand,
)
from presentation.modules.user_management.application.commands.create_user.dto import (
    CreateUserResultDTO,
)
from presentation.modules.user_management.application.commands.create_user.unit_of_work import (
    UserCreationConflictError,
    UserCreationUnitOfWorkFactory,
)
from presentation.modules.user_management.application.commands.create_user.validator import (
    CreateUserCommandValidator,
)
from shared.kernel.result import Result


class CreateUserHandler:
    """Handles the create user command."""

    def __init__(
        self,
        unit_of_work_factory: UserCreationUnitOfWorkFactory,
        password_service: PasswordService,
        validator: CreateUserCommandValidator | None = None,
    ) -> None:
        self._unit_of_work_factory = unit_of_work_factory
        self._password_service = password_service
        self._validator = validator or CreateUserCommandValidator()

    def handle(self, command: CreateUserCommand) -> Result[CreateUserResultDTO]:
        """Create a user and return a safe DTO."""
        validation = self._validator.validate(command)
        if validation.is_failure:
            return Result.failure(validation.error)

        normalized = validation.value
        try:
            username = Username(normalized.username)
            email = Email(normalized.email)
        except InvalidUsernameException:
            return Result.failure("Login informado e invalido.")
        except InvalidEmailException:
            return Result.failure("E-mail informado e invalido.")

        with self._unit_of_work_factory.create() as unit_of_work:
            if unit_of_work.users.get_by_username(username) is not None:
                unit_of_work.rollback()
                return Result.failure("Este login ja esta em uso.")
            if unit_of_work.users.get_by_email(email) is not None:
                unit_of_work.rollback()
                return Result.failure("Este e-mail ja esta em uso.")

            try:
                password_hash = self._password_service.hash_password(normalized.password)
                user = User.create(
                    username,
                    email,
                    password_hash,
                    full_name=normalized.full_name,
                )
                unit_of_work.users.add(user)
                unit_of_work.commit()
            except UserCreationConflictError:
                unit_of_work.rollback()
                return Result.failure("Este login ou e-mail ja esta em uso.")
            except InvalidPasswordException as exc:
                unit_of_work.rollback()
                return Result.failure(str(exc))
            except (IdentityDomainException, ValidationException) as exc:
                unit_of_work.rollback()
                return Result.failure(str(exc))

        return Result.success(CreateUserResultDTO.from_domain(user))
