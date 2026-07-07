from __future__ import annotations

from datetime import UTC, datetime

from domain.identity.value_objects import PermissionCode
from shared.kernel.entity import Entity
from shared.kernel.identity import Identity


class Permission(Entity[Identity]):
    """Permission entity used to authorize application actions."""

    __slots__ = ("_code", "_description", "_created_at", "_updated_at")

    def __init__(
        self,
        entity_id: Identity,
        code: PermissionCode,
        description: str,
        created_at: datetime,
        updated_at: datetime,
    ) -> None:
        super().__init__(entity_id)
        self._code = code
        self._description = description.strip()
        self._created_at = created_at
        self._updated_at = updated_at

    @classmethod
    def create(cls, code: PermissionCode, description: str) -> Permission:
        """Create a permission."""
        now = datetime.now(UTC)
        return cls(Identity.new(), code, description, now, now)

    @property
    def code(self) -> PermissionCode:
        """Return permission code."""
        return self._code

    @property
    def description(self) -> str:
        """Return permission description."""
        return self._description

    @property
    def created_at(self) -> datetime:
        """Return creation timestamp."""
        return self._created_at

    @property
    def updated_at(self) -> datetime:
        """Return update timestamp."""
        return self._updated_at
