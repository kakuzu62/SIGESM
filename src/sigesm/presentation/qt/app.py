from __future__ import annotations

import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPixmap
from PySide6.QtWidgets import QApplication, QSplashScreen

from sigesm.infrastructure.di import ApplicationContainer
from presentation.framework.application import DesktopContext
from presentation.framework.controllers import LoginController
from presentation.framework.navigation import NavigationService
from presentation.framework.services import NotificationService
from presentation.framework.themes import ThemeManager, ThemeMode
from presentation.framework.viewmodels import LoginViewModel
from presentation.framework.views import LoginDialog, MainWindow
from presentation.framework.workspace import WorkspaceManager


def run_qt_application(container: ApplicationContainer) -> int:
    qt_app = QApplication.instance() or QApplication(sys.argv)
    if not isinstance(qt_app, QApplication):
        raise RuntimeError("QApplication could not be initialized.")

    splash = _show_splash()
    splash.showMessage(
        "Inicializando SIGESM...",
        Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignCenter,
        QColor("#f9fafb"),
    )
    qt_app.processEvents()
    container.health_check().execute()

    context = DesktopContext(
        navigation=NavigationService(),
        workspace=WorkspaceManager(),
        themes=ThemeManager(),
        notifications=NotificationService(),
    )
    context.themes.apply(qt_app, ThemeMode.DARK)
    splash.showMessage(
        "Carregando autenticacao...",
        Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignCenter,
        QColor("#f9fafb"),
    )
    qt_app.processEvents()

    login = LoginDialog(LoginViewModel(LoginController(container.authenticate_user_handler())))
    splash.finish(login)
    if login.exec() != LoginDialog.DialogCode.Accepted or login.authentication is None:
        return 0

    window = MainWindow(context=context, authentication=login.authentication)
    window.show()
    return qt_app.exec()


def _show_splash() -> QSplashScreen:
    pixmap = QPixmap(520, 300)
    pixmap.fill(QColor("#111827"))
    splash = QSplashScreen(pixmap)
    splash.show()
    return splash
