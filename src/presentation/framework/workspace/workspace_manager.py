from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from PySide6.QtWidgets import QWidget


@dataclass(frozen=True, slots=True)
class WorkspaceDocument:
    """Descriptor for an opened workspace document or view."""

    key: str
    title: str
    route: str


class WorkspaceManager:
    """Loads, unloads and caches workspace views."""

    def __init__(self, cache_views: bool = True) -> None:
        self._cache_views = cache_views
        self._documents: dict[str, WorkspaceDocument] = {}
        self._views: dict[str, QWidget] = {}
        self._current_key: str | None = None

    def load_view(self, key: str, factory: Callable[[], QWidget]) -> QWidget:
        """Load a workspace view, reusing a cached instance when enabled."""
        view = self._views.get(key)
        if view is None or not self._cache_views:
            view = factory()
            if self._cache_views:
                self._views[key] = view
        self._current_key = key
        return view

    def unload_current(self) -> None:
        """Unload the current view reference."""
        self._current_key = None

    def current_view(self) -> QWidget | None:
        """Return the current cached view when available."""
        if self._current_key is None:
            return None
        return self._views.get(self._current_key)

    def clear(self) -> None:
        """Clear workspace documents and view cache."""
        self._documents.clear()
        self._views.clear()
        self._current_key = None

    def open(self, document: WorkspaceDocument) -> None:
        """Open or replace a workspace document descriptor."""
        self._documents[document.key] = document

    def close(self, key: str) -> None:
        """Close a workspace document descriptor."""
        self._documents.pop(key, None)
        self._views.pop(key, None)
        if self._current_key == key:
            self._current_key = None

    @property
    def documents(self) -> tuple[WorkspaceDocument, ...]:
        """Return opened workspace documents."""
        return tuple(self._documents.values())
