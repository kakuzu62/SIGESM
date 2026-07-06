from __future__ import annotations

from datetime import date

from domain.service_scale.value_objects import ScaleType
from shared.kernel.domain_event import DomainEvent
from shared.kernel.identity import Identity


class ScaleGenerated(DomainEvent):
    """Event raised when a service scale generation run finishes."""

    __slots__ = ("generation_id", "scale_id", "scale_type", "service_date", "selected_count")

    def __init__(
        self,
        generation_id: Identity,
        scale_id: Identity,
        scale_type: ScaleType,
        service_date: date,
        selected_count: int,
    ) -> None:
        super().__init__()
        self.generation_id = generation_id
        self.scale_id = scale_id
        self.scale_type = scale_type
        self.service_date = service_date
        self.selected_count = selected_count
