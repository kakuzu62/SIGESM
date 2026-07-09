from __future__ import annotations

from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class MilitaryView(QWidget):
    """Military registry placeholder view."""

    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)
        title = QLabel("Cadastro de Militares")
        title.setObjectName("title")
        message = QLabel("Modulo funcional previsto para a Release 2.2.")
        layout.addWidget(title)
        layout.addWidget(message)
        layout.addStretch()
