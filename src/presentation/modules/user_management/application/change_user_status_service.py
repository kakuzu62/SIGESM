from __future__ import annotations

from presentation.modules.user_management.application.commands.change_user_status import (
    ChangeUserActiveStatusCommand,
    ChangeUserActiveStatusHandler,
    ChangeUserActiveStatusResultDTO,
    UserStatusUnitOfWorkFactory,
)
from shared.kernel.result import Result


class ChangeUserActiveStatusService:
    """Application facade for activating and deactivating users."""

    def __init__(self, unit_of_work_factory: UserStatusUnitOfWorkFactory) -> None:
        self._handler = ChangeUserActiveStatusHandler(unit_of_work_factory)

    def change_status(
        self, command: ChangeUserActiveStatusCommand
    ) -> Result[ChangeUserActiveStatusResultDTO]:
        """Change the requested user's active status."""
        return self._handler.handle(command)
