from __future__ import annotations

from collections.abc import Callable

from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from application.identity.dto import AuthenticationDTO
from presentation.framework.application import DesktopContext
from presentation.framework.navigation import NavigationItem
from presentation.framework.themes import ThemeMode
from presentation.framework.workspace import WorkspaceDocument
from presentation.modules.dashboard import DashboardView
from presentation.modules.military import MilitaryView
from presentation.modules.organization import OrganizationView
from presentation.modules.scale import ScaleView
from presentation.modules.settings import SettingsView


class MainWindow(QMainWindow):
    """Main SIGESM desktop shell."""

    def __init__(self, context: DesktopContext, authentication: AuthenticationDTO) -> None:
        super().__init__()
        self._context = context
        self._authentication = authentication
        self._stack = QStackedWidget()
        self._view_factories: dict[str, Callable[[], QWidget]] = {
            "dashboard": DashboardView,
            "organization": OrganizationView,
            "military": MilitaryView,
            "scale": ScaleView,
            "settings": SettingsView,
        }
        self._views: dict[str, QWidget] = {}
        self._sidebar = QFrame()
        self._status = QLabel("Pronto")
        self._build()
        self._register_modules()
        self.navigate("dashboard")

    def navigate(self, key: str) -> None:
        """Navigate to a registered module."""
        item = self._context.navigation.navigate(key)
        view = self._views.get(key)
        if view is None:
            view = self._view_factories[key]()
            self._views[key] = view
            self._stack.addWidget(view)
        self._context.workspace.open(
            WorkspaceDocument(key=item.key, title=item.label, route=item.route)
        )
        self._stack.setCurrentWidget(view)
        self._status.setText(f"Modulo ativo: {item.label}")

    def _build(self) -> None:
        self.setWindowTitle("SIGESM Enterprise")
        self.resize(1280, 780)
        root = QWidget()
        root_layout = QVBoxLayout(root)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.addWidget(self._build_header())
        body = QHBoxLayout()
        body.addWidget(self._build_sidebar())
        body.addWidget(self._stack, stretch=1)
        root_layout.addLayout(body, stretch=1)
        root_layout.addWidget(self._build_status_bar())
        self.setCentralWidget(root)

    def _build_header(self) -> QFrame:
        header = QFrame()
        header.setObjectName("header")
        layout = QHBoxLayout(header)
        title = QLabel("SIGESM Enterprise")
        title.setObjectName("title")
        user = QLabel(f"Usuario: {self._authentication.user_id}")
        theme = QPushButton("Alternar tema")
        theme.clicked.connect(self._toggle_theme)
        exit_button = QPushButton("Sair")
        exit_button.clicked.connect(self.close)
        layout.addWidget(title)
        layout.addStretch()
        layout.addWidget(user)
        layout.addWidget(theme)
        layout.addWidget(exit_button)
        return header

    def _build_sidebar(self) -> QFrame:
        self._sidebar.setObjectName("sidebar")
        layout = QVBoxLayout(self._sidebar)
        for key, label in (
            ("dashboard", "Dashboard"),
            ("organization", "Organizacao"),
            ("military", "Militares"),
            ("scale", "Escalas"),
            ("settings", "Configuracoes"),
        ):
            button = QPushButton(label)
            button.clicked.connect(lambda _checked=False, route=key: self.navigate(route))
            layout.addWidget(button)
        layout.addStretch()
        return self._sidebar

    def _build_status_bar(self) -> QFrame:
        status = QFrame()
        status.setObjectName("statusBar")
        layout = QHBoxLayout(status)
        layout.addWidget(self._status)
        layout.addStretch()
        layout.addWidget(QLabel("Banco validado | Plataforma Desktop 2.0"))
        return status

    def _register_modules(self) -> None:
        for key, label in (
            ("dashboard", "Dashboard"),
            ("organization", "Organizacao Militar"),
            ("military", "Cadastro de Militares"),
            ("scale", "Escalas"),
            ("settings", "Configuracoes"),
        ):
            self._context.navigation.register(NavigationItem(key=key, label=label, route=f"/{key}"))

    def _toggle_theme(self) -> None:
        app = QApplication.instance()
        if isinstance(app, QApplication):
            mode = self._context.themes.toggle_light_dark(app)
            label = "Claro" if mode == ThemeMode.LIGHT else "Escuro"
            self._status.setText(f"Tema alterado: {label}")
