from __future__ import annotations

from domain.identity.repositories import IRoleRepository
from presentation.modules.user_management.application.queries.list_available_roles import (
    ListAvailableRolesHandler,
    ListAvailableRolesQuery,
    RoleListItemDTO,
)
from shared.kernel.result import Result


class ListAvailableRolesService:
    """Application facade for listing assignable roles."""

    def __init__(self, roles: IRoleRepository) -> None:
        self._handler = ListAvailableRolesHandler(roles)

    def list_roles(
        self, query: ListAvailableRolesQuery | None = None
    ) -> Result[tuple[RoleListItemDTO, ...]]:
        """List available roles."""
        return self._handler.handle(query or ListAvailableRolesQuery())
