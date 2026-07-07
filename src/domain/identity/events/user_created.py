from __future__ import annotations

from domain.identity.value_objects import Email, Username
from shared.kernel.domain_event import DomainEvent
from shared.kernel.identity import Identity


class UserCreated(DomainEvent):
    """Event raised when a user is created."""

    __slots__ = ("user_id", "username", "email")

    def __init__(self, user_id: Identity, username: Username, email: Email) -> None:
        super().__init__()
        self.user_id = user_id
        self.username = username
        self.email = email
