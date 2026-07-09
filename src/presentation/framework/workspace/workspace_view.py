from __future__ import annotations

from PySide6.QtWidgets import QVBoxLayout, QWidget


class WorkspaceView(QWidget):
    """Central widget that displays the active module view."""

    def __init__(self) -> None:
        super().__init__()
        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._current: QWidget | None = None

    def set_view(self, view: QWidget) -> None:
        """Display the provided view as the active workspace content."""
        if self._current is not None:
            self._layout.removeWidget(self._current)
            self._current.setParent(None)
        self._current = view
        self._layout.addWidget(view)

    def clear(self) -> None:
        """Remove the active view."""
        if self._current is not None:
            self._layout.removeWidget(self._current)
            self._current.setParent(None)
            self._current = None
