from __future__ import annotations

from datetime import UTC, datetime

from domain.identity.value_objects import Username
from shared.kernel.entity import Entity
from shared.kernel.identity import Identity


class AuthenticationAttempt(Entity[Identity]):
    """Auditable authentication attempt."""

    __slots__ = ("_username", "_successful", "_reason", "_occurred_at")

    def __init__(
        self,
        entity_id: Identity,
        username: Username,
        successful: bool,
        reason: str,
        occurred_at: datetime,
    ) -> None:
        super().__init__(entity_id)
        self._username = username
        self._successful = successful
        self._reason = reason.strip()
        self._occurred_at = occurred_at

    @classmethod
    def record(cls, username: Username, successful: bool, reason: str) -> AuthenticationAttempt:
        """Create an authentication attempt audit record."""
        return cls(Identity.new(), username, successful, reason, datetime.now(UTC))

    @property
    def username(self) -> Username:
        """Return attempted username."""
        return self._username

    @property
    def successful(self) -> bool:
        """Return whether authentication succeeded."""
        return self._successful

    @property
    def reason(self) -> str:
        """Return attempt reason."""
        return self._reason

    @property
    def occurred_at(self) -> datetime:
        """Return attempt timestamp."""
        return self._occurred_at
