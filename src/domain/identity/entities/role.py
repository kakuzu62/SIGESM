from __future__ import annotations

from datetime import UTC, datetime

from domain.identity.entities.permission import Permission
from domain.identity.exceptions import IdentityDomainException
from shared.kernel.entity import Entity
from shared.kernel.identity import Identity


class Role(Entity[Identity]):
    """Role entity grouping permissions for a user profile."""

    __slots__ = ("_name", "_description", "_permissions", "_created_at", "_updated_at")

    def __init__(
        self,
        entity_id: Identity,
        name: str,
        description: str,
        permissions: tuple[Permission, ...],
        created_at: datetime,
        updated_at: datetime,
    ) -> None:
        super().__init__(entity_id)
        normalized_name = name.strip()
        if not normalized_name:
            raise IdentityDomainException("Role name is required.")

        self._name = normalized_name
        self._description = description.strip()
        self._permissions = permissions
        self._created_at = created_at
        self._updated_at = updated_at

    @classmethod
    def create(cls, name: str, description: str = "") -> Role:
        """Create a role without permissions."""
        now = datetime.now(UTC)
        return cls(Identity.new(), name, description, (), now, now)

    @property
    def name(self) -> str:
        """Return role name."""
        return self._name

    @property
    def description(self) -> str:
        """Return role description."""
        return self._description

    @property
    def permissions(self) -> tuple[Permission, ...]:
        """Return role permissions."""
        return self._permissions

    @property
    def created_at(self) -> datetime:
        """Return creation timestamp."""
        return self._created_at

    @property
    def updated_at(self) -> datetime:
        """Return update timestamp."""
        return self._updated_at

    def add_permission(self, permission: Permission) -> None:
        """Add a permission to the role."""
        if permission in self._permissions:
            return

        self._permissions = (*self._permissions, permission)
        self._touch()

    def remove_permission(self, permission: Permission) -> None:
        """Remove a permission from the role."""
        self._permissions = tuple(item for item in self._permissions if item != permission)
        self._touch()

    def _touch(self) -> None:
        self._updated_at = datetime.now(UTC)
