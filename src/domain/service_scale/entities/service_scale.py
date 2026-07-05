from __future__ import annotations

from datetime import UTC, datetime

from domain.service_scale.entities.service_assignment import ServiceAssignment
from domain.service_scale.entities.service_role import ServiceRole
from domain.service_scale.events import ServiceAssignmentCancelled, ServiceAssignmentCreated
from domain.service_scale.exceptions import ServiceScaleDomainException
from domain.service_scale.value_objects import AssignmentStatus, ScaleType, ServiceDate, ServiceRoleName
from shared.kernel.aggregate_root import AggregateRoot
from shared.kernel.identity import Identity


class ServiceScale(AggregateRoot[Identity]):
    """Aggregate root that manages 24-hour service scale assignments."""

    __slots__ = ("_scale_type", "_roles", "_assignments", "_created_at", "_updated_at")

    def __init__(
        self,
        entity_id: Identity,
        scale_type: ScaleType,
        roles: tuple[ServiceRole, ...],
        assignments: tuple[ServiceAssignment, ...],
        created_at: datetime,
        updated_at: datetime,
    ) -> None:
        super().__init__(entity_id)
        self._scale_type = scale_type
        self._roles = list(roles)
        self._assignments = list(assignments)
        self._created_at = created_at
        self._updated_at = updated_at

    @classmethod
    def create(cls, scale_type: ScaleType) -> ServiceScale:
        """Create a service scale by type."""
        now = datetime.now(UTC)
        return cls(
            entity_id=Identity.new(),
            scale_type=scale_type,
            roles=(),
            assignments=(),
            created_at=now,
            updated_at=now,
        )

    @property
    def scale_type(self) -> ScaleType:
        """Return scale type."""
        return self._scale_type

    @property
    def roles(self) -> tuple[ServiceRole, ...]:
        """Return service roles."""
        return tuple(self._roles)

    @property
    def assignments(self) -> tuple[ServiceAssignment, ...]:
        """Return service assignments."""
        return tuple(self._assignments)

    @property
    def created_at(self) -> datetime:
        """Return creation timestamp."""
        return self._created_at

    @property
    def updated_at(self) -> datetime:
        """Return last update timestamp."""
        return self._updated_at

    def add_service_role(self, name: ServiceRoleName) -> ServiceRole:
        """Add a role required by this service scale."""
        role = ServiceRole.create(name)
        self._roles.append(role)
        self._touch()
        return role

    def create_assignment(
        self,
        military_id: Identity,
        service_date: ServiceDate,
        role_id: Identity,
    ) -> ServiceAssignment:
        """Create a military assignment for a service date and role."""
        self._ensure_role_exists(role_id)
        assignment = ServiceAssignment.create(
            military_id=military_id,
            service_date=service_date,
            scale_type=self._scale_type,
            role_id=role_id,
        )
        self._assignments.append(assignment)
        self.add_domain_event(
            ServiceAssignmentCreated(
                assignment_id=assignment.id,
                military_id=assignment.military_id,
                service_scale_id=self.id,
            )
        )
        self._touch()
        return assignment

    def cancel_assignment(self, assignment_id: Identity, reason: str) -> None:
        """Cancel a scheduled assignment with a reason."""
        assignment = self._get_assignment(assignment_id)
        assignment.cancel(reason)
        self.add_domain_event(
            ServiceAssignmentCancelled(
                assignment_id=assignment.id,
                service_scale_id=self.id,
                reason=assignment.cancellation_reason or reason.strip(),
            )
        )
        self._touch()

    def complete_assignment(self, assignment_id: Identity) -> None:
        """Mark an assignment as completed."""
        assignment = self._get_assignment(assignment_id)
        assignment.complete()
        self._touch()

    def scheduled_assignments_for(self, military_id: Identity) -> tuple[ServiceAssignment, ...]:
        """Return scheduled assignments for one military identity."""
        return tuple(
            assignment
            for assignment in self._assignments
            if assignment.military_id == military_id and assignment.status == AssignmentStatus.SCHEDULED
        )

    def _ensure_role_exists(self, role_id: Identity) -> None:
        if not any(role.id == role_id for role in self._roles):
            raise ServiceScaleDomainException("Service role does not belong to this scale.")

    def _get_assignment(self, assignment_id: Identity) -> ServiceAssignment:
        for assignment in self._assignments:
            if assignment.id == assignment_id:
                return assignment
        raise ServiceScaleDomainException("Service assignment was not found.")

    def _touch(self) -> None:
        """Update modification timestamp."""
        self._updated_at = datetime.now(UTC)
