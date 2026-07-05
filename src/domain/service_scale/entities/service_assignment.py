from __future__ import annotations

from datetime import UTC, datetime

from domain.service_scale.exceptions import InvalidAssignmentOperationException
from domain.service_scale.value_objects import AssignmentStatus, ScaleType, ServiceDate
from shared.kernel.entity import Entity
from shared.kernel.identity import Identity


class ServiceAssignment(Entity[Identity]):
    """Entity representing one military person assigned to a 24-hour service."""

    __slots__ = (
        "_military_id",
        "_service_date",
        "_scale_type",
        "_role_id",
        "_status",
        "_created_at",
        "_updated_at",
        "_cancellation_reason",
    )

    def __init__(
        self,
        entity_id: Identity,
        military_id: Identity,
        service_date: ServiceDate,
        scale_type: ScaleType,
        role_id: Identity,
        status: AssignmentStatus,
        created_at: datetime,
        updated_at: datetime,
        cancellation_reason: str | None = None,
    ) -> None:
        super().__init__(entity_id)
        self._military_id = military_id
        self._service_date = service_date
        self._scale_type = scale_type
        self._role_id = role_id
        self._status = status
        self._created_at = created_at
        self._updated_at = updated_at
        self._cancellation_reason = cancellation_reason

    @classmethod
    def create(
        cls,
        military_id: Identity,
        service_date: ServiceDate,
        scale_type: ScaleType,
        role_id: Identity,
    ) -> ServiceAssignment:
        """Create a scheduled service assignment."""
        now = datetime.now(UTC)
        return cls(
            entity_id=Identity.new(),
            military_id=military_id,
            service_date=service_date,
            scale_type=scale_type,
            role_id=role_id,
            status=AssignmentStatus.SCHEDULED,
            created_at=now,
            updated_at=now,
        )

    @property
    def military_id(self) -> Identity:
        """Return assigned military identity."""
        return self._military_id

    @property
    def service_date(self) -> ServiceDate:
        """Return service date."""
        return self._service_date

    @property
    def scale_type(self) -> ScaleType:
        """Return assignment scale type."""
        return self._scale_type

    @property
    def role_id(self) -> Identity:
        """Return assigned role identity."""
        return self._role_id

    @property
    def status(self) -> AssignmentStatus:
        """Return assignment status."""
        return self._status

    @property
    def created_at(self) -> datetime:
        """Return creation timestamp."""
        return self._created_at

    @property
    def updated_at(self) -> datetime:
        """Return last update timestamp."""
        return self._updated_at

    @property
    def cancellation_reason(self) -> str | None:
        """Return cancellation reason when cancelled."""
        return self._cancellation_reason

    def cancel(self, reason: str) -> None:
        """Cancel a scheduled assignment with a required reason."""
        if self._status != AssignmentStatus.SCHEDULED:
            raise InvalidAssignmentOperationException("Only scheduled assignments can be cancelled.")
        normalized_reason = reason.strip()
        if not normalized_reason:
            raise InvalidAssignmentOperationException("Cancellation reason is required.")
        self._status = AssignmentStatus.CANCELLED
        self._cancellation_reason = normalized_reason
        self._touch()

    def complete(self) -> None:
        """Mark a scheduled assignment as completed."""
        if self._status != AssignmentStatus.SCHEDULED:
            raise InvalidAssignmentOperationException("Only scheduled assignments can be completed.")
        self._status = AssignmentStatus.COMPLETED
        self._touch()

    def replace(self) -> None:
        """Mark a scheduled assignment as replaced."""
        if self._status != AssignmentStatus.SCHEDULED:
            raise InvalidAssignmentOperationException("Only scheduled assignments can be replaced.")
        self._status = AssignmentStatus.REPLACED
        self._touch()

    def _touch(self) -> None:
        """Update modification timestamp."""
        self._updated_at = datetime.now(UTC)
