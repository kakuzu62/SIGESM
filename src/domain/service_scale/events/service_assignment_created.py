from __future__ import annotations

from shared.kernel.domain_event import DomainEvent
from shared.kernel.identity import Identity


class ServiceAssignmentCreated(DomainEvent):
    """Event raised when a service assignment is created."""

    __slots__ = ("assignment_id", "military_id", "service_scale_id")

    def __init__(self, assignment_id: Identity, military_id: Identity, service_scale_id: Identity) -> None:
        super().__init__()
        self.assignment_id = assignment_id
        self.military_id = military_id
        self.service_scale_id = service_scale_id
