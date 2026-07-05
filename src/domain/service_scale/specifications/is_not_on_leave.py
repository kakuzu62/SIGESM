from __future__ import annotations

from domain.military.value_objects import MilitaryStatus
from domain.service_scale.services.eligibility_reason import EligibilityReason
from domain.service_scale.specifications.eligibility_context import EligibilityContext


class MilitaryNotOnLeaveSpecification:
    """Specification that rejects military persons on leave."""

    reason = EligibilityReason.ON_LEAVE

    def is_satisfied_by(self, candidate: EligibilityContext) -> bool:
        """Return whether the military person is not on leave."""
        return candidate.military.status != MilitaryStatus.ON_LEAVE
