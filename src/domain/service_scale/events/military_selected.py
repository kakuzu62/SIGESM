from __future__ import annotations

from datetime import date

from domain.service_scale.value_objects import ScaleType
from shared.kernel.domain_event import DomainEvent
from shared.kernel.identity import Identity


class MilitarySelected(DomainEvent):
    """Event raised when a military person is selected for a generated scale."""

    __slots__ = ("generation_id", "military_id", "scale_type", "service_date")

    def __init__(
        self,
        generation_id: Identity,
        military_id: Identity,
        scale_type: ScaleType,
        service_date: date,
    ) -> None:
        super().__init__()
        self.generation_id = generation_id
        self.military_id = military_id
        self.scale_type = scale_type
        self.service_date = service_date
