from __future__ import annotations

from domain.identity.repositories import IRoleRepository
from presentation.modules.user_management.application.queries.list_available_roles.dto import (
    RoleListItemDTO,
)
from presentation.modules.user_management.application.queries.list_available_roles.query import (
    ListAvailableRolesQuery,
)
from shared.kernel.result import Result


class ListAvailableRolesHandler:
    """Handles available role listing."""

    def __init__(self, roles: IRoleRepository) -> None:
        self._roles = roles

    def handle(self, query: ListAvailableRolesQuery) -> Result[tuple[RoleListItemDTO, ...]]:
        """Return roles sorted by name."""
        roles = self._roles.list() if query.include_inactive else self._roles.list_active()
        ordered = tuple(sorted(roles, key=lambda role: role.name.lower()))
        return Result.success(tuple(RoleListItemDTO.from_domain(role) for role in ordered))
