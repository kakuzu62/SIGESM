from __future__ import annotations

from shared.kernel.domain_event import DomainEvent
from shared.kernel.identity import Identity


class ServiceSaleRejected(DomainEvent):
    """Event raised when a service sale is rejected."""

    __slots__ = ("reasons", "sale_id")

    def __init__(self, sale_id: Identity, reasons: tuple[str, ...]) -> None:
        super().__init__()
        self.sale_id = sale_id
        self.reasons = reasons
