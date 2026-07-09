from __future__ import annotations

import logging

from presentation.modules.user_management.domain.events import UserAuditEvent


class UserAuditService:
    """Records auditable user management actions."""

    def __init__(self) -> None:
        self._logger = logging.getLogger(__name__)
        self._events: list[UserAuditEvent] = []

    def record(self, action: str, user_id: str, actor_id: str | None = None) -> None:
        """Record an audit action."""
        event = UserAuditEvent.create(action, user_id, actor_id)
        self._events.append(event)
        self._logger.info("User audit action recorded: %s for %s", action, user_id)

    @property
    def events(self) -> tuple[UserAuditEvent, ...]:
        """Return recorded audit events."""
        return tuple(self._events)
