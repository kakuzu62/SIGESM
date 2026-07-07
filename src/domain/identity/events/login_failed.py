from __future__ import annotations

from domain.identity.value_objects import Username
from shared.kernel.domain_event import DomainEvent


class LoginFailed(DomainEvent):
    """Event raised when an authentication attempt fails."""

    __slots__ = ("username", "reason")

    def __init__(self, username: Username, reason: str) -> None:
        super().__init__()
        self.username = username
        self.reason = reason
