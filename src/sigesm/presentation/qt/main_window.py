from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QMainWindow, QStatusBar

from sigesm.infrastructure.di import ApplicationContainer


class MainWindow(QMainWindow):
    def __init__(self, container: ApplicationContainer) -> None:
        super().__init__()
        self._container = container
        self.setWindowTitle(container.settings.app_name)
        self.resize(1120, 720)
        self.setCentralWidget(self._build_content())
        self.setStatusBar(self._build_status_bar())

    def _build_content(self) -> QLabel:
        label = QLabel(self._container.settings.app_name)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setObjectName("mainTitle")
        return label

    def _build_status_bar(self) -> QStatusBar:
        status_bar = QStatusBar()
        result = self._container.health_check().execute()
        status = "Banco de dados conectado" if result.database_available else "Banco indisponivel"
        status_bar.showMessage(status)
        return status_bar
