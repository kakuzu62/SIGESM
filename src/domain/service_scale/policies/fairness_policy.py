from __future__ import annotations

from domain.military.entities import MilitaryPerson
from domain.service_scale.entities import ServiceAssignment
from domain.service_scale.services.fairness_service import FairnessService
from domain.service_scale.value_objects import ServiceDate


class FairnessPolicy:
    """Policy that applies fairness ordering to eligible candidates."""

    def __init__(self, service: FairnessService | None = None) -> None:
        self._service = service or FairnessService()

    def order(
        self,
        candidates: tuple[MilitaryPerson, ...],
        service_date: ServiceDate,
        history: tuple[ServiceAssignment, ...],
    ) -> tuple[MilitaryPerson, ...]:
        """Order candidates according to fairness service metrics."""
        return self._service.order_by_fairness(candidates, service_date, history)
