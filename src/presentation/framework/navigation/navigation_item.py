from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from PySide6.QtWidgets import QWidget


@dataclass(frozen=True, slots=True)
class NavigationItem:
    """Navigation item registered in the desktop shell."""

    key: str
    title: str
    factory: Callable[[], QWidget] | None = None
    icon: str | None = None
    requires_authentication: bool = True
    order: int = 0
    route: str | None = None
    permission: str | None = None

    @property
    def label(self) -> str:
        """Return the user-facing title."""
        return self.title

    @property
    def resolved_route(self) -> str:
        """Return the configured route or a route derived from the key."""
        return self.route or f"/{self.key}"
