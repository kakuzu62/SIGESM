from __future__ import annotations

from domain.military.value_objects import MilitaryStatus
from domain.service_scale.services.eligibility_reason import EligibilityReason
from domain.service_scale.specifications.eligibility_context import EligibilityContext


class MilitaryActiveSpecification:
    """Specification that requires an active military person."""

    reason = EligibilityReason.MILITARY_INACTIVE

    def is_satisfied_by(self, candidate: EligibilityContext) -> bool:
        """Return whether the military person is active."""
        return candidate.military.status == MilitaryStatus.ACTIVE
