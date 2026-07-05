from __future__ import annotations

from domain.service_scale.services.eligibility_reason import EligibilityReason
from domain.service_scale.specifications.eligibility_context import EligibilityContext


class MilitaryCompatibleScaleSpecification:
    """Specification that validates scale compatibility for a military person."""

    reason = EligibilityReason.SCALE_NOT_ALLOWED

    def is_satisfied_by(self, candidate: EligibilityContext) -> bool:
        """Return whether the military person is allowed in the target scale."""
        allowed_scales = candidate.allowed_scale_ids_by_military.get(candidate.military.id)
        return allowed_scales is None or candidate.service_scale.id in allowed_scales
