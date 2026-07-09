from __future__ import annotations

from presentation.framework.notifications.notification import Notification


class NotificationService:
    """Stores desktop notifications for the shell."""

    def __init__(self) -> None:
        self._items: list[Notification] = []

    def publish(self, notification: Notification) -> None:
        """Publish a notification."""
        self._items.append(notification)

    @property
    def items(self) -> tuple[Notification, ...]:
        """Return published notifications."""
        return tuple(self._items)
