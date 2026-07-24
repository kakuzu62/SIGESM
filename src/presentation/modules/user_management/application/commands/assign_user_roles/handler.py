from __future__ import annotations

from collections.abc import Sequence

from domain.identity.entities import Role, User
from domain.identity.exceptions import IdentityDomainException
from presentation.modules.user_management.application.commands.assign_user_roles.command import (
    AssignUserRolesCommand,
)
from presentation.modules.user_management.application.commands.assign_user_roles.dto import (
    AssignUserRolesResultDTO,
)
from presentation.modules.user_management.application.commands.assign_user_roles.unit_of_work import (
    UserRolesPersistenceError,
    UserRolesUnitOfWorkFactory,
)
from presentation.modules.user_management.application.commands.assign_user_roles.validator import (
    AssignUserRolesCommandValidator,
)
from shared.kernel.identity import Identity
from shared.kernel.result import Result


class AssignUserRolesHandler:
    """Handles full replacement of a user's assigned roles."""

    _ADMIN_NORMALIZED_NAME = "ADMINISTRADOR"

    def __init__(
        self,
        unit_of_work_factory: UserRolesUnitOfWorkFactory,
        validator: AssignUserRolesCommandValidator | None = None,
    ) -> None:
        self._unit_of_work_factory = unit_of_work_factory
        self._validator = validator or AssignUserRolesCommandValidator()

    def handle(self, command: AssignUserRolesCommand) -> Result[AssignUserRolesResultDTO]:
        """Assign selected roles to a target user."""
        validation = self._validator.validate(command)
        if validation.is_failure:
            return Result.failure(validation.error)

        normalized = validation.value
        target_id = Identity.from_string(normalized.target_user_id)
        role_ids = tuple(Identity.from_string(role_id) for role_id in normalized.role_ids)

        with self._unit_of_work_factory.create() as unit_of_work:
            user = unit_of_work.users.get_by_id(target_id)
            if user is None:
                unit_of_work.rollback()
                return Result.failure("Usuario nao encontrado.")

            roles = unit_of_work.roles.get_by_ids(role_ids)
            if len(roles) != len(role_ids):
                unit_of_work.rollback()
                return Result.failure("Um ou mais perfis nao foram encontrados.")
            if any(not role.active for role in roles):
                unit_of_work.rollback()
                return Result.failure("Perfis inativos nao podem ser atribuidos.")

            admin_role = self._find_admin_role(unit_of_work.roles.list())
            if admin_role is not None and self._removes_last_active_admin(
                admin_role,
                user,
                roles,
                unit_of_work.roles.count_active_users_with_role(admin_role.id),
            ):
                unit_of_work.rollback()
                return Result.failure("O sistema deve manter ao menos um administrador ativo.")

            try:
                user.set_roles(roles)
                unit_of_work.users.update(user)
                unit_of_work.commit()
            except UserRolesPersistenceError:
                unit_of_work.rollback()
                return Result.failure("Nao foi possivel atualizar os perfis do usuario.")
            except IdentityDomainException as exc:
                unit_of_work.rollback()
                return Result.failure(str(exc))

        return Result.success(AssignUserRolesResultDTO.from_domain(user))

    def _find_admin_role(self, roles: Sequence[Role]) -> Role | None:
        return next(
            (role for role in roles if role.normalized_name == self._ADMIN_NORMALIZED_NAME),
            None,
        )

    @staticmethod
    def _removes_last_active_admin(
        admin_role: Role,
        user: User,
        new_roles: tuple[Role, ...],
        active_admin_count: int,
    ) -> bool:
        currently_admin = any(role.id == admin_role.id for role in user.roles)
        remains_admin = any(role.id == admin_role.id for role in new_roles)
        return user.active and currently_admin and not remains_admin and active_admin_count <= 1
