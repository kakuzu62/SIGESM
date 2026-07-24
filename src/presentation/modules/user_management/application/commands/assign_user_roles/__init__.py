"""Application slice for assigning roles to users."""

from presentation.modules.user_management.application.commands.assign_user_roles.command import (
    AssignUserRolesCommand,
)
from presentation.modules.user_management.application.commands.assign_user_roles.dto import (
    AssignUserRolesResultDTO,
)
from presentation.modules.user_management.application.commands.assign_user_roles.handler import (
    AssignUserRolesHandler,
)
from presentation.modules.user_management.application.commands.assign_user_roles.unit_of_work import (
    UserRolesPersistenceError,
    UserRolesUnitOfWork,
    UserRolesUnitOfWorkFactory,
)
from presentation.modules.user_management.application.commands.assign_user_roles.validator import (
    AssignUserRolesCommandValidator,
)

__all__ = [
    "AssignUserRolesCommand",
    "AssignUserRolesCommandValidator",
    "AssignUserRolesHandler",
    "AssignUserRolesResultDTO",
    "UserRolesPersistenceError",
    "UserRolesUnitOfWork",
    "UserRolesUnitOfWorkFactory",
]
