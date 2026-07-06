from __future__ import annotations

from typing import Protocol

from domain.military.entities import MilitaryPerson
from domain.service_scale.engines.generation_context import GenerationContext


class ScaleStrategy(Protocol):
    """Strategy interface for scale-specific candidate ordering rules."""

    def apply(
        self,
        context: GenerationContext,
        candidates: tuple[MilitaryPerson, ...],
    ) -> tuple[MilitaryPerson, ...]:
        """Apply scale-specific ordering or filtering."""
        raise NotImplementedError
