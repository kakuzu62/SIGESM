from __future__ import annotations

from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class ScaleView(QWidget):
    """Service scale placeholder view."""

    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)
        title = QLabel("Escalas")
        title.setObjectName("title")
        message = QLabel("Modulo de escalas sera conectado aos engines de dominio.")
        layout.addWidget(title)
        layout.addWidget(message)
        layout.addStretch()
