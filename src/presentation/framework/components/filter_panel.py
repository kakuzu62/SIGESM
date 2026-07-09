from __future__ import annotations

from collections.abc import Callable

from PySide6.QtWidgets import QComboBox, QHBoxLayout, QLabel, QWidget


class FilterPanel(QWidget):
    """Reusable status filter panel."""

    def __init__(self, on_status_changed: Callable[[str], None]) -> None:
        super().__init__()
        self._on_status_changed = on_status_changed
        self._status = QComboBox()
        self._status.addItems(["ALL", "ACTIVE", "INACTIVE"])
        self._status.currentTextChanged.connect(self._on_status_changed)
        layout = QHBoxLayout(self)
        layout.addWidget(QLabel("Status"))
        layout.addWidget(self._status)
        layout.addStretch()
