from __future__ import annotations

from domain.military.value_objects import MilitaryStatus
from domain.service_scale.services.eligibility_reason import EligibilityReason
from domain.service_scale.specifications.eligibility_context import EligibilityContext


class MilitaryNotRestrictedSpecification:
    """Specification that rejects restricted military persons."""

    reason = EligibilityReason.RESTRICTED

    def is_satisfied_by(self, candidate: EligibilityContext) -> bool:
        """Return whether the military person is not restricted."""
        return candidate.military.status != MilitaryStatus.RESTRICTED
