from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime


@dataclass(frozen=True, slots=True)
class UserAuditEvent:
    """Audit event emitted by user management actions."""

    action: str
    user_id: str
    actor_id: str | None
    occurred_at: datetime

    @classmethod
    def create(cls, action: str, user_id: str, actor_id: str | None = None) -> UserAuditEvent:
        """Create an audit event."""
        return cls(action=action, user_id=user_id, actor_id=actor_id, occurred_at=datetime.now(UTC))
