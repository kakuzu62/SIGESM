from __future__ import annotations

from domain.identity.services import PasswordService
from presentation.modules.user_management.application.commands.reset_password import (
    ResetPasswordCommand,
    ResetPasswordHandler,
    ResetPasswordResultDTO,
    ResetPasswordUnitOfWorkFactory,
)
from shared.kernel.result import Result


class ResetPasswordService:
    """Application facade for administrator password reset."""

    def __init__(
        self,
        unit_of_work_factory: ResetPasswordUnitOfWorkFactory,
        password_service: PasswordService,
    ) -> None:
        self._handler = ResetPasswordHandler(unit_of_work_factory, password_service)

    def reset_password(self, command: ResetPasswordCommand) -> Result[ResetPasswordResultDTO]:
        """Reset the requested user's password."""
        return self._handler.handle(command)
