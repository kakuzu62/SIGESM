from __future__ import annotations

from shared.kernel.domain_event import DomainEvent
from shared.kernel.identity import Identity


class OfficialSwapApproved(DomainEvent):
    """Event raised when an official swap is approved."""

    __slots__ = ("approved_by", "swap_id")

    def __init__(self, swap_id: Identity, approved_by: Identity) -> None:
        super().__init__()
        self.swap_id = swap_id
        self.approved_by = approved_by
