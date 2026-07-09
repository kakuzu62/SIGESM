from __future__ import annotations

from presentation.framework.navigation.navigation_history import NavigationHistory
from presentation.framework.navigation.navigation_item import NavigationItem


class NavigationService:
    """Navigation registry and history controller for the desktop shell."""

    def __init__(self) -> None:
        self._items: dict[str, NavigationItem] = {}
        self._history = NavigationHistory()

    def register_item(self, item: NavigationItem) -> None:
        """Register a navigation item."""
        self._items[item.key] = item

    def register(self, item: NavigationItem) -> None:
        """Register a navigation item using the legacy method name."""
        self.register_item(item)

    def navigate_to(self, key: str) -> NavigationItem:
        """Navigate to a registered item."""
        item = self._items[key]
        self._history.record(item.key)
        return item

    def navigate(self, key: str) -> NavigationItem:
        """Navigate to a registered item using the legacy method name."""
        return self.navigate_to(key)

    def go_back(self) -> NavigationItem | None:
        """Navigate to the previous item when available."""
        key = self._history.back()
        return self._items[key] if key is not None else None

    def go_forward(self) -> NavigationItem | None:
        """Navigate to the next item when available."""
        key = self._history.forward()
        return self._items[key] if key is not None else None

    def current_item(self) -> NavigationItem | None:
        """Return the active navigation item."""
        key = self._history.current
        return self._items[key] if key is not None else None

    def items(self) -> tuple[NavigationItem, ...]:
        """Return registered navigation items ordered for display."""
        return tuple(sorted(self._items.values(), key=lambda item: item.order))

    @property
    def current_route(self) -> str | None:
        """Return the current route."""
        item = self.current_item()
        return item.resolved_route if item is not None else None
