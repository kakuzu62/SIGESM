from __future__ import annotations

from dataclasses import dataclass

from domain.military.entities import MilitaryPerson
from domain.service_scale.engines.generation_statistics import GenerationStatistics
from domain.service_scale.services.eligibility_reason import EligibilityReason
from shared.kernel.domain_event import DomainEvent
from shared.kernel.identity import Identity


@dataclass(frozen=True, slots=True)
class SkippedCandidate:
    """Military candidate skipped during scale generation."""

    military_id: Identity
    reasons: tuple[EligibilityReason, ...]


@dataclass(frozen=True, slots=True)
class GenerationResult:
    """Result returned by the scale generation engine."""

    generation_id: Identity
    selected_military: tuple[MilitaryPerson, ...]
    skipped_military: tuple[SkippedCandidate, ...]
    skip_reasons: dict[Identity, tuple[EligibilityReason, ...]]
    statistics: GenerationStatistics
    events: tuple[DomainEvent, ...]
    processing_time_seconds: float
