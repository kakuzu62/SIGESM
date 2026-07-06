from __future__ import annotations

from shared.kernel.domain_event import DomainEvent
from shared.kernel.identity import Identity


class ServiceSaleApproved(DomainEvent):
    """Event raised when a service sale is approved."""

    __slots__ = ("approved_by", "sale_id")

    def __init__(self, sale_id: Identity, approved_by: Identity) -> None:
        super().__init__()
        self.sale_id = sale_id
        self.approved_by = approved_by
