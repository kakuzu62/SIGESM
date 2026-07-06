from __future__ import annotations

from shared.kernel.domain_event import DomainEvent
from shared.kernel.identity import Identity


class OfficialSwapRejected(DomainEvent):
    """Event raised when an official swap is rejected."""

    __slots__ = ("reasons", "swap_id")

    def __init__(self, swap_id: Identity, reasons: tuple[str, ...]) -> None:
        super().__init__()
        self.swap_id = swap_id
        self.reasons = reasons
