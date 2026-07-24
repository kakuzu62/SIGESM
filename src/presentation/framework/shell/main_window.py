from __future__ import annotations

from collections.abc import Callable

from PySide6.QtWidgets import QApplication, QHBoxLayout, QMainWindow, QVBoxLayout, QWidget

from presentation.framework.application.desktop_context import DesktopContext
from presentation.framework.navigation import NavigationItem
from presentation.framework.shell.header_bar import HeaderBar
from presentation.framework.shell.shell_view_model import ShellViewModel
from presentation.framework.shell.side_bar import SideBar
from presentation.framework.shell.status_bar import StatusBar
from presentation.framework.themes import ThemeMode
from presentation.framework.workspace import WorkspaceDocument, WorkspaceManager, WorkspaceView
from presentation.modules.dashboard import DashboardView
from presentation.modules.military import MilitaryView
from presentation.modules.organization import OrganizationView
from presentation.modules.scale import ScaleView
from presentation.modules.settings import SettingsView
from presentation.modules.user_management.presentation.viewmodels import UserListViewModel
from presentation.modules.user_management.presentation.views import UserListView


class MainWindow(QMainWindow):
    """Main SIGESM desktop shell."""

    def __init__(
        self,
        context: DesktopContext,
        view_model: ShellViewModel,
        workspace_manager: WorkspaceManager | None = None,
    ) -> None:
        super().__init__()
        self._context = context
        self._view_model = view_model
        self._workspace_manager = workspace_manager or context.workspace
        self._workspace = WorkspaceView()
        self._status = StatusBar()
        self._view_factories: dict[str, Callable[[], QWidget]] = {
            "dashboard": DashboardView,
            "users": self._users_view,
            "organization": OrganizationView,
            "military": MilitaryView,
            "scale": ScaleView,
            "settings": SettingsView,
        }
        self._register_modules()
        self._build()
        self.navigate("dashboard")

    def navigate(self, key: str) -> None:
        """Navigate to a registered module."""
        item = self._context.navigation.navigate_to(key)
        factory = item.factory or self._view_factories[key]
        view = self._workspace_manager.load_view(key, factory)
        self._workspace.set_view(view)
        self._workspace_manager.open(
            WorkspaceDocument(key=item.key, title=item.title, route=item.resolved_route)
        )
        self._status.set_message(f"Modulo ativo: {item.title}")

    def _build(self) -> None:
        self.setWindowTitle("SIGESM Enterprise")
        self.resize(1280, 780)
        root = QWidget()
        root_layout = QHBoxLayout(root)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.addWidget(SideBar(self._context.navigation.items(), self.navigate))
        center = QWidget()
        center_layout = QVBoxLayout(center)
        center_layout.setContentsMargins(0, 0, 0, 0)
        center_layout.addWidget(
            HeaderBar(self._view_model.user_label, self._toggle_theme, self._close_application)
        )
        center_layout.addWidget(self._workspace, stretch=1)
        center_layout.addWidget(self._status)
        root_layout.addWidget(center, stretch=1)
        self.setCentralWidget(root)

    def _register_modules(self) -> None:
        for order, (key, title, factory) in enumerate(
            (
                ("dashboard", "Dashboard", DashboardView),
                ("users", "Usuarios", self._users_view),
                ("organization", "Organizacao Militar", OrganizationView),
                ("military", "Cadastro de Militares", MilitaryView),
                ("scale", "Escalas", ScaleView),
                ("settings", "Configuracoes", SettingsView),
            ),
            start=1,
        ):
            self._context.navigation.register_item(
                NavigationItem(
                    key=key,
                    title=title,
                    factory=factory,
                    route=f"/{key}",
                    order=order,
                )
            )

    def _toggle_theme(self) -> None:
        app = QApplication.instance()
        if isinstance(app, QApplication):
            mode = self._context.themes.toggle_light_dark(app)
            label = "Claro" if mode == ThemeMode.LIGHT else "Escuro"
            self._status.set_message(f"Tema alterado: {label}")

    def _close_application(self) -> None:
        self.close()

    def _users_view(self) -> QWidget:
        return UserListView(
            UserListViewModel(
                self._context.user_listing,
                self._context.user_creation,
                self._context.user_editing,
                self._context.user_status,
                self._context.password_reset,
                self._context.role_listing,
                self._context.role_assignment,
                self._view_model.user_id,
            )
        )
