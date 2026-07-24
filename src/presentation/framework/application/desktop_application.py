from __future__ import annotations

import logging
import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPixmap
from PySide6.QtWidgets import QApplication, QSplashScreen

from presentation.framework.application.application_lifecycle import ApplicationLifecycle
from presentation.framework.application.desktop_context import DesktopContext
from presentation.framework.controllers import LoginController
from presentation.framework.navigation import NavigationService
from presentation.framework.notifications import NotificationService
from presentation.framework.shell import MainWindow, ShellViewModel
from presentation.framework.themes import ThemeManager, ThemeMode
from presentation.framework.viewmodels import LoginViewModel
from presentation.framework.views import LoginDialog
from presentation.framework.workspace import WorkspaceManager
from sigesm.infrastructure.di import ApplicationContainer


class DesktopApplication:
    """Coordinates the executable SIGESM desktop application."""

    def __init__(
        self,
        container: ApplicationContainer,
        lifecycle: ApplicationLifecycle | None = None,
    ) -> None:
        self._container = container
        self._lifecycle = lifecycle or ApplicationLifecycle()
        self._logger = logging.getLogger(__name__)

    def run(self) -> int:
        """Start the desktop application."""
        return self._lifecycle.run_guarded(self._run)

    def _run(self) -> int:
        qt_app = QApplication.instance() or QApplication(sys.argv)
        if not isinstance(qt_app, QApplication):
            raise RuntimeError("QApplication could not be initialized.")

        qt_app.setApplicationName("SIGESM Enterprise")
        splash = self._show_splash()
        self._show_splash_message(qt_app, splash, "Inicializando SIGESM...")
        self._container.health_check().execute()

        context = DesktopContext(
            navigation=NavigationService(),
            workspace=WorkspaceManager(),
            themes=ThemeManager(),
            notifications=NotificationService(),
            user_listing=self._container.user_listing_service(),
            user_creation=self._container.create_user_service(),
            user_editing=self._container.edit_user_service(),
            user_status=self._container.change_user_status_service(),
            password_reset=self._container.reset_password_service(),
            role_listing=self._container.list_available_roles_service(),
            role_assignment=self._container.assign_user_roles_service(),
        )
        context.themes.apply(qt_app, ThemeMode.DARK)
        self._show_splash_message(qt_app, splash, "Carregando autenticacao...")

        login = LoginDialog(
            LoginViewModel(LoginController(self._container.authenticate_user_handler()))
        )
        splash.finish(login)
        if login.exec() != LoginDialog.DialogCode.Accepted or login.authentication is None:
            self._logger.info("Desktop login cancelled.")
            return 0

        window = MainWindow(context=context, view_model=ShellViewModel(login.authentication))
        window.show()
        return qt_app.exec()

    @staticmethod
    def _show_splash() -> QSplashScreen:
        pixmap = QPixmap(520, 300)
        pixmap.fill(QColor("#111827"))
        splash = QSplashScreen(pixmap)
        splash.show()
        return splash

    @staticmethod
    def _show_splash_message(
        application: QApplication,
        splash: QSplashScreen,
        message: str,
    ) -> None:
        splash.showMessage(
            message,
            Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignCenter,
            QColor("#f9fafb"),
        )
        application.processEvents()
