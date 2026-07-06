from __future__ import annotations

from abc import abstractmethod
from collections.abc import Sequence

from domain.contracts.repository import IRepository
from domain.service_exchange.entities import OfficialSwap, ServiceSale
from shared.kernel.identity import Identity


class IServiceExchangeRepository(IRepository[OfficialSwap | ServiceSale, Identity]):
    """Repository contract for service exchange aggregates."""

    @abstractmethod
    def list_official_swaps(self) -> Sequence[OfficialSwap]:
        """Return official swap aggregates."""
        raise NotImplementedError

    @abstractmethod
    def list_service_sales(self) -> Sequence[ServiceSale]:
        """Return service sale aggregates."""
        raise NotImplementedError
