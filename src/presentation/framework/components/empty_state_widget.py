from __future__ import annotations

from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class EmptyStateWidget(QWidget):
    """Reusable empty state widget."""

    def __init__(self, message: str) -> None:
        super().__init__()
        layout = QVBoxLayout(self)
        label = QLabel(message)
        label.setObjectName("subtitle")
        layout.addWidget(label)
