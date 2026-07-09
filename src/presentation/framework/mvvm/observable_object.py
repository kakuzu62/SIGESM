from __future__ import annotations

from collections.abc import Callable


class ObservableObject:
    """Base object with property change notification support."""

    def __init__(self) -> None:
        self._property_changed_handlers: list[Callable[[str], None]] = []

    def subscribe(self, handler: Callable[[str], None]) -> None:
        """Subscribe to property change notifications."""
        self._property_changed_handlers.append(handler)

    def unsubscribe(self, handler: Callable[[str], None]) -> None:
        """Remove a previously subscribed property change handler."""
        if handler in self._property_changed_handlers:
            self._property_changed_handlers.remove(handler)

    def notify_property_changed(self, property_name: str) -> None:
        """Notify listeners that a property has changed."""
        for handler in tuple(self._property_changed_handlers):
            handler(property_name)
