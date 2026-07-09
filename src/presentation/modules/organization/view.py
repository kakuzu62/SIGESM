from __future__ import annotations

from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class OrganizationView(QWidget):
    """Organization module placeholder view."""

    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)
        title = QLabel("Organizacao Militar")
        title.setObjectName("title")
        message = QLabel("Modulo funcional previsto para a Release 2.1.")
        layout.addWidget(title)
        layout.addWidget(message)
        layout.addStretch()
