from __future__ import annotations

from domain.service_scale.services.eligibility_reason import EligibilityReason
from domain.service_scale.specifications.eligibility_context import EligibilityContext


class MilitaryNotManuallyBlockedSpecification:
    """Specification that rejects military persons blocked by explicit decision."""

    reason = EligibilityReason.MANUAL_BLOCK

    def is_satisfied_by(self, candidate: EligibilityContext) -> bool:
        """Return whether the military person is not manually blocked."""
        return candidate.military.id not in candidate.manually_blocked_military_ids
