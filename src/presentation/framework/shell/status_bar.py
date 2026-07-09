from __future__ import annotations

from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel


class StatusBar(QFrame):
    """Bottom status bar for the desktop shell."""

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("statusBar")
        self._message = QLabel("Pronto")
        layout = QHBoxLayout(self)
        layout.addWidget(self._message)
        layout.addStretch()
        layout.addWidget(QLabel("Banco validado | Plataforma Desktop 2.0"))

    def set_message(self, message: str) -> None:
        """Update the status message."""
        self._message.setText(message)
