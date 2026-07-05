from __future__ import annotations

from abc import abstractmethod
from collections.abc import Sequence

from domain.contracts.repository import IRepository
from domain.service_scale.entities import ServiceAssignment, ServiceScale
from domain.service_scale.value_objects import ScaleType, ServiceDate
from shared.kernel.identity import Identity


class IServiceScaleRepository(IRepository[ServiceScale, Identity]):
    """Repository contract for service scale aggregates."""

    @abstractmethod
    def list_by_type(self, scale_type: ScaleType) -> Sequence[ServiceScale]:
        """Return service scales by type."""
        raise NotImplementedError

    @abstractmethod
    def list_assignments_for_military(self, military_id: Identity) -> Sequence[ServiceAssignment]:
        """Return assignments associated with one military identity."""
        raise NotImplementedError

    @abstractmethod
    def list_assignments_for_date(self, service_date: ServiceDate) -> Sequence[ServiceAssignment]:
        """Return assignments associated with a service date."""
        raise NotImplementedError
