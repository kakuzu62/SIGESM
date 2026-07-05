from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication

from sigesm.infrastructure.di import ApplicationContainer
from sigesm.presentation.qt.main_window import MainWindow


def run_qt_application(container: ApplicationContainer) -> int:
    qt_app = QApplication.instance() or QApplication(sys.argv)
    window = MainWindow(container=container)
    window.show()
    return qt_app.exec()
