from __future__ import annotations

from datetime import date

from domain.service_scale.services.eligibility_reason import EligibilityReason
from domain.service_scale.value_objects import ScaleType
from shared.kernel.domain_event import DomainEvent
from shared.kernel.identity import Identity


class MilitarySkipped(DomainEvent):
    """Event raised when a military candidate is skipped during generation."""

    __slots__ = ("generation_id", "military_id", "reasons", "scale_type", "service_date")

    def __init__(
        self,
        generation_id: Identity,
        military_id: Identity,
        scale_type: ScaleType,
        service_date: date,
        reasons: tuple[EligibilityReason, ...],
    ) -> None:
        super().__init__()
        self.generation_id = generation_id
        self.military_id = military_id
        self.scale_type = scale_type
        self.service_date = service_date
        self.reasons = reasons
