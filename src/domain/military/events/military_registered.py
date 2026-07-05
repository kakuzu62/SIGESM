from __future__ import annotations

from shared.kernel.domain_event import DomainEvent
from shared.kernel.identity import Identity


class MilitaryRegistered(DomainEvent):
    """Event raised when a military person is registered."""

    __slots__ = ("military_person_id", "military_id")

    def __init__(self, military_person_id: Identity, military_id: str) -> None:
        super().__init__()
        self.military_person_id = military_person_id
        self.military_id = military_id
