from __future__ import annotations

from presentation.modules.user_management.application.commands.assign_user_roles import (
    AssignUserRolesCommand,
    AssignUserRolesHandler,
    AssignUserRolesResultDTO,
    UserRolesUnitOfWorkFactory,
)
from shared.kernel.result import Result


class AssignUserRolesService:
    """Application facade for assigning roles to users."""

    def __init__(self, unit_of_work_factory: UserRolesUnitOfWorkFactory) -> None:
        self._handler = AssignUserRolesHandler(unit_of_work_factory)

    def assign_roles(self, command: AssignUserRolesCommand) -> Result[AssignUserRolesResultDTO]:
        """Assign roles to a user."""
        return self._handler.handle(command)
