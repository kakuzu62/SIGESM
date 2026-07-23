from __future__ import annotations

from domain.identity.services import PasswordService
from presentation.modules.user_management.application.commands.create_user import (
    CreateUserCommand,
    CreateUserHandler,
    CreateUserResultDTO,
)
from presentation.modules.user_management.application.commands.create_user.unit_of_work import (
    UserCreationUnitOfWorkFactory,
)
from shared.kernel.result import Result


class CreateUserService:
    """Application facade for user creation."""

    def __init__(
        self,
        unit_of_work_factory: UserCreationUnitOfWorkFactory,
        password_service: PasswordService,
    ) -> None:
        self._handler = CreateUserHandler(unit_of_work_factory, password_service)

    def create_user(self, command: CreateUserCommand) -> Result[CreateUserResultDTO]:
        """Create a user through the application command handler."""
        return self._handler.handle(command)
