from __future__ import annotations

from datetime import UTC, datetime

from domain.service_scale.value_objects import ServiceRoleName
from shared.kernel.entity import Entity
from shared.kernel.identity import Identity


class ServiceRole(Entity[Identity]):
    """Entity representing a role required in a service scale."""

    __slots__ = ("_name", "_created_at", "_updated_at")

    def __init__(
        self,
        entity_id: Identity,
        name: ServiceRoleName,
        created_at: datetime,
        updated_at: datetime,
    ) -> None:
        super().__init__(entity_id)
        self._name = name
        self._created_at = created_at
        self._updated_at = updated_at

    @classmethod
    def create(cls, name: ServiceRoleName) -> ServiceRole:
        """Create a service role."""
        now = datetime.now(UTC)
        return cls(entity_id=Identity.new(), name=name, created_at=now, updated_at=now)

    @property
    def name(self) -> ServiceRoleName:
        """Return role name."""
        return self._name

    @property
    def created_at(self) -> datetime:
        """Return creation timestamp."""
        return self._created_at

    @property
    def updated_at(self) -> datetime:
        """Return last update timestamp."""
        return self._updated_at
