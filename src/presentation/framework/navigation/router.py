from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class NavigationItem:
    """Navigation item registered in the desktop shell."""

    key: str
    label: str
    route: str
    permission: str | None = None


class NavigationService:
    """In-memory navigation registry for the desktop shell."""

    def __init__(self) -> None:
        self._items: dict[str, NavigationItem] = {}
        self._current_route: str | None = None

    def register(self, item: NavigationItem) -> None:
        """Register a navigation item."""
        self._items[item.key] = item

    def navigate(self, key: str) -> NavigationItem:
        """Navigate to an item by key and return it."""
        item = self._items[key]
        self._current_route = item.route
        return item

    @property
    def items(self) -> tuple[NavigationItem, ...]:
        """Return registered navigation items."""
        return tuple(self._items.values())

    @property
    def current_route(self) -> str | None:
        """Return current route."""
        return self._current_route
