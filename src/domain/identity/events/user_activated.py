from __future__ import annotations

from shared.kernel.domain_event import DomainEvent
from shared.kernel.identity import Identity


class UserActivated(DomainEvent):
    """Event raised when a user is activated."""

    __slots__ = ("user_id",)

    def __init__(self, user_id: Identity) -> None:
        super().__init__()
        self.user_id = user_id
