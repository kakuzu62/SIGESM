from __future__ import annotations

from domain.military.entities import MilitaryPerson
from domain.service_scale.engines.generation_context import GenerationContext


class BlackScaleStrategy:
    """Generation strategy for PRETA service scales."""

    def apply(
        self,
        context: GenerationContext,
        candidates: tuple[MilitaryPerson, ...],
    ) -> tuple[MilitaryPerson, ...]:
        """Return candidates unchanged for standard PRETA scale generation."""
        return candidates
