from __future__ import annotations

from shared.kernel.domain_event import DomainEvent
from shared.kernel.identity import Identity


class ServiceAssignmentCancelled(DomainEvent):
    """Event raised when a service assignment is cancelled."""

    __slots__ = ("assignment_id", "reason", "service_scale_id")

    def __init__(self, assignment_id: Identity, service_scale_id: Identity, reason: str) -> None:
        super().__init__()
        self.assignment_id = assignment_id
        self.service_scale_id = service_scale_id
        self.reason = reason
