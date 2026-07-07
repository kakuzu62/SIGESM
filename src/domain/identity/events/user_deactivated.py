from __future__ import annotations

from shared.kernel.domain_event import DomainEvent
from shared.kernel.identity import Identity


class UserDeactivated(DomainEvent):
    """Event raised when a user is deactivated."""

    __slots__ = ("user_id", "reason")

    def __init__(self, user_id: Identity, reason: str) -> None:
        super().__init__()
        self.user_id = user_id
        self.reason = reason
