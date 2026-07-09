from __future__ import annotations

from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class SettingsView(QWidget):
    """Settings placeholder view."""

    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)
        title = QLabel("Configuracoes")
        title.setObjectName("title")
        message = QLabel("Tema, preferencias e parametros operacionais ficarao aqui.")
        layout.addWidget(title)
        layout.addWidget(message)
        layout.addStretch()
