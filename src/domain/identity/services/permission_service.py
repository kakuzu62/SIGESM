from __future__ import annotations

from domain.identity.entities import User
from domain.identity.value_objects import PermissionCode


class PermissionService:
    """Domain service responsible for permission checks."""

    def has_permission(self, user: User, permission_code: PermissionCode) -> bool:
        """Return whether a user has a permission through any assigned role."""
        return any(
            permission.code == permission_code
            for role in user.roles
            for permission in role.permissions
        )
