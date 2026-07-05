from __future__ import annotations

from dataclasses import dataclass

from domain.service_scale.policies import MinimumRestPolicy
from domain.service_scale.value_objects import RestPeriod
from shared.kernel.specification import Specification


@dataclass(frozen=True, slots=True)
class MinimumRestEvaluation:
    """Input used to evaluate minimum rest for a service assignment."""

    rest_period: RestPeriod
    allow_one_by_one_exception: bool = False


class MinimumRestSatisfiedSpecification(Specification[MinimumRestEvaluation]):
    """Specification that validates minimum rest for a candidate assignment."""

    def __init__(self, policy: MinimumRestPolicy | None = None) -> None:
        self._policy = policy or MinimumRestPolicy()

    def is_satisfied_by(self, candidate: MinimumRestEvaluation) -> bool:
        """Return whether candidate rest satisfies the configured policy."""
        return self._policy.is_satisfied(
            rest_period=candidate.rest_period,
            allow_one_by_one_exception=candidate.allow_one_by_one_exception,
        )
