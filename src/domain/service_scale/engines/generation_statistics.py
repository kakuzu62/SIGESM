from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class GenerationStatistics:
    """Statistics produced by a scale generation run."""

    analyzed_count: int
    eligible_count: int
    skipped_count: int
    selected_count: int
    execution_time_seconds: float
    verification_count: int
