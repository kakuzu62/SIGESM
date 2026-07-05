from __future__ import annotations

from domain.service_scale.services.eligibility_reason import EligibilityReason
from domain.service_scale.specifications.eligibility_context import EligibilityContext


class MilitaryQualifiedForRoleSpecification:
    """Specification that validates role compatibility for a military person."""

    reason = EligibilityReason.ROLE_NOT_ALLOWED

    def is_satisfied_by(self, candidate: EligibilityContext) -> bool:
        """Return whether the military person is allowed to perform the role."""
        allowed_roles = candidate.allowed_role_ids_by_military.get(candidate.military.id)
        return allowed_roles is None or candidate.service_role.id in allowed_roles
