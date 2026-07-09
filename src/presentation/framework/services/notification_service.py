from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Notification:
    """Desktop notification message."""

    title: str
    message: str
    severity: str = "info"


class NotificationService:
    """In-memory notification service for the desktop shell."""

    def __init__(self) -> None:
        self._items: list[Notification] = []

    def publish(self, notification: Notification) -> None:
        """Publish a notification."""
        self._items.append(notification)

    @property
    def items(self) -> tuple[Notification, ...]:
        """Return published notifications."""
        return tuple(self._items)
