from __future__ import annotations

from shared.kernel.domain_event import DomainEvent
from shared.kernel.identity import Identity


class OrganizationCreated(DomainEvent):
    """Event raised when an organization is created."""

    __slots__ = ("organization_id", "code")

    def __init__(self, organization_id: Identity, code: str) -> None:
        super().__init__()
        self.organization_id = organization_id
        self.code = code
