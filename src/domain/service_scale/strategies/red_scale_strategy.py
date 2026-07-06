from __future__ import annotations

from domain.military.entities import MilitaryPerson
from domain.service_scale.engines.generation_context import GenerationContext


class RedScaleStrategy:
    """Generation strategy for VERMELHA service scales."""

    def apply(
        self,
        context: GenerationContext,
        candidates: tuple[MilitaryPerson, ...],
    ) -> tuple[MilitaryPerson, ...]:
        """Return candidates ordered deterministically for VERMELHA scale generation."""
        return tuple(sorted(candidates, key=lambda candidate: candidate.military_id.value))
