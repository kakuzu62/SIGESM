from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from shared.kernel.identity import Identity


@dataclass(frozen=True, slots=True)
class TieBreakCandidate:
    """Candidate data used for deterministic service scale tie-breaking."""

    military_id: Identity
    last_service_at: datetime | None
    total_assignments: int
    audit_key: str


class TieBreakPolicy:
    """Deterministic tie-break policy prepared for auditable automatic selection."""

    def choose(self, candidates: tuple[TieBreakCandidate, ...]) -> TieBreakCandidate:
        """Choose the best candidate using stable auditable ordering."""
        if not candidates:
            raise ValueError("Tie-break requires at least one candidate.")

        return sorted(
            candidates,
            key=lambda candidate: (
                candidate.total_assignments,
                candidate.last_service_at or datetime.min,
                candidate.audit_key,
                str(candidate.military_id),
            ),
        )[0]
