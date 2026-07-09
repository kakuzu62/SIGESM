from __future__ import annotations

from collections.abc import Callable


class ObservableViewModel:
    """Base view model with change notification hooks."""

    def __init__(self) -> None:
        self._listeners: list[Callable[[str], None]] = []

    def subscribe(self, listener: Callable[[str], None]) -> None:
        """Subscribe a listener to property changes."""
        self._listeners.append(listener)

    def notify_changed(self, property_name: str) -> None:
        """Notify listeners that a property changed."""
        for listener in tuple(self._listeners):
            listener(property_name)
