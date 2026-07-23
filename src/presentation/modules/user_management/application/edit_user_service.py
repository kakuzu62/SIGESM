from __future__ import annotations

from presentation.modules.user_management.application.commands.update_user import (
    UpdateUserCommand,
    UpdateUserHandler,
    UpdateUserResultDTO,
)
from presentation.modules.user_management.application.commands.update_user.unit_of_work import (
    UserUpdateUnitOfWorkFactory,
)
from shared.kernel.result import Result


class EditUserService:
    """Application facade for user profile editing."""

    def __init__(self, unit_of_work_factory: UserUpdateUnitOfWorkFactory) -> None:
        self._handler = UpdateUserHandler(unit_of_work_factory)

    def update_user(self, command: UpdateUserCommand) -> Result[UpdateUserResultDTO]:
        """Update a user through the application command handler."""
        return self._handler.handle(command)
