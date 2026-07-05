from __future__ import annotations

from dataclasses import dataclass

from domain.service_scale.specifications.minimum_rest_satisfied import (
    MinimumRestEvaluation,
    MinimumRestSatisfiedSpecification,
)
from domain.service_scale.value_objects import RestPeriod
from shared.kernel.identity import Identity
from shared.kernel.specification import Specification


@dataclass(frozen=True, slots=True)
class MilitaryScaleAvailability:
    """Input used to determine whether a military person is available for scale."""

    military_id: Identity
    rest_period: RestPeriod
    has_conflicting_assignment: bool
    allow_one_by_one_exception: bool = False


class MilitaryAvailableForScaleSpecification(Specification[MilitaryScaleAvailability]):
    """Specification that validates availability for service scale assignment."""

    def __init__(self, minimum_rest: MinimumRestSatisfiedSpecification | None = None) -> None:
        self._minimum_rest = minimum_rest or MinimumRestSatisfiedSpecification()

    def is_satisfied_by(self, candidate: MilitaryScaleAvailability) -> bool:
        """Return whether candidate is available for a new service assignment."""
        if candidate.has_conflicting_assignment:
            return False

        return self._minimum_rest.is_satisfied_by(
            MinimumRestEvaluation(
                rest_period=candidate.rest_period,
                allow_one_by_one_exception=candidate.allow_one_by_one_exception,
            )
        )
