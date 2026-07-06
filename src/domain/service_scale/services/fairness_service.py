from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, time

from domain.military.entities import MilitaryPerson
from domain.service_scale.entities import ServiceAssignment
from domain.service_scale.value_objects import AssignmentStatus, ServiceDate


@dataclass(frozen=True, slots=True)
class FairnessScore:
    """Fairness score used to order generation candidates."""

    military: MilitaryPerson
    days_without_service: int
    last_service_at: datetime | None
    total_assignments: int


class FairnessService:
    """Domain service that calculates fairness metrics for scale generation."""

    def score(
        self,
        military: MilitaryPerson,
        service_date: ServiceDate,
        history: tuple[ServiceAssignment, ...],
    ) -> FairnessScore:
        """Calculate fairness score for one military candidate."""
        assignments = tuple(
            assignment
            for assignment in history
            if assignment.military_id == military.id
            and assignment.status in {AssignmentStatus.SCHEDULED, AssignmentStatus.COMPLETED}
        )
        last_service_at = self._last_service_at(assignments)
        if last_service_at is None:
            days_without_service = 999_999
        else:
            days_without_service = (service_date.value - last_service_at.date()).days

        return FairnessScore(
            military=military,
            days_without_service=days_without_service,
            last_service_at=last_service_at,
            total_assignments=len(assignments),
        )

    def order_by_fairness(
        self,
        candidates: tuple[MilitaryPerson, ...],
        service_date: ServiceDate,
        history: tuple[ServiceAssignment, ...],
    ) -> tuple[MilitaryPerson, ...]:
        """Order candidates by fairness, preferring those with fewer services and longer rest."""
        scores = tuple(self.score(candidate, service_date, history) for candidate in candidates)
        ordered = sorted(
            scores,
            key=lambda score: (
                score.total_assignments,
                -score.days_without_service,
                str(score.military.id),
            ),
        )
        return tuple(score.military for score in ordered)

    @staticmethod
    def _last_service_at(assignments: tuple[ServiceAssignment, ...]) -> datetime | None:
        if not assignments:
            return None

        latest = max(assignments, key=lambda assignment: assignment.service_date.value)
        return datetime.combine(latest.service_date.value, time.min)
