from __future__ import annotations

from datetime import date

from domain.service_scale.value_objects import ScaleType
from shared.kernel.domain_event import DomainEvent
from shared.kernel.identity import Identity


class MilitaryDeclaredEligible(DomainEvent):
    """Event raised when a military person is declared eligible for a service."""

    __slots__ = ("military_id", "scale_id", "scale_type", "service_date")

    def __init__(
        self,
        military_id: Identity,
        scale_id: Identity,
        scale_type: ScaleType,
        service_date: date,
    ) -> None:
        super().__init__()
        self.military_id = military_id
        self.scale_id = scale_id
        self.scale_type = scale_type
        self.service_date = service_date
