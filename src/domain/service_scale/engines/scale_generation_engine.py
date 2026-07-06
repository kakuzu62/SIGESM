from __future__ import annotations

from domain.service_scale.engines.generation_context import GenerationContext
from domain.service_scale.engines.generation_result import GenerationResult, SkippedCandidate
from domain.service_scale.policies.generation_policy import GenerationPolicy
from shared.kernel.identity import Identity


class ScaleGenerationEngine:
    """Domain service responsible for automatic service scale generation."""

    def __init__(self, policy: GenerationPolicy | None = None) -> None:
        self._policy = policy or GenerationPolicy()

    def generate(self, context: GenerationContext) -> GenerationResult:
        """Generate a service scale selection from an immutable context."""
        generation_id = Identity.new()
        policy_result = self._policy.generate(generation_id, context)
        skipped = tuple(
            SkippedCandidate(military_id=event.military_id, reasons=event.reasons)
            for event in policy_result.skipped_events
        )
        return GenerationResult(
            generation_id=generation_id,
            selected_military=policy_result.selected,
            skipped_military=skipped,
            skip_reasons={candidate.military_id: candidate.reasons for candidate in skipped},
            statistics=policy_result.statistics,
            events=policy_result.events,
            processing_time_seconds=policy_result.elapsed_seconds,
        )
