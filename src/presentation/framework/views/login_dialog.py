from __future__ import annotations

from application.identity.dto import AuthenticationDTO
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QFormLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)

from presentation.framework.viewmodels import LoginViewModel


class LoginDialog(QDialog):
    """Authentication dialog shown before the main shell."""

    def __init__(self, view_model: LoginViewModel) -> None:
        super().__init__()
        self._view_model = view_model
        self._authentication: AuthenticationDTO | None = None
        self._username = QLineEdit("admin")
        self._password = QLineEdit("Admin#123")
        self._message = QLabel("")
        self._build()
        self._view_model.subscribe(self._on_view_model_changed)

    @property
    def authentication(self) -> AuthenticationDTO | None:
        """Return authentication data after a successful login."""
        return self._authentication

    def _build(self) -> None:
        self.setWindowTitle("SIGESM Enterprise - Login")
        self.setModal(True)
        self.setMinimumWidth(420)
        self._password.setEchoMode(QLineEdit.EchoMode.Password)
        title = QLabel("SIGESM Enterprise")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle = QLabel("Acesso ao sistema")
        subtitle.setObjectName("subtitle")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        form = QFormLayout()
        form.addRow("Usuario", self._username)
        form.addRow("Senha", self._password)
        button = QPushButton("Entrar")
        button.setObjectName("primaryButton")
        button.clicked.connect(self._login)
        layout = QVBoxLayout(self)
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addLayout(form)
        layout.addWidget(self._message)
        layout.addWidget(button)

    def _login(self) -> None:
        result = self._view_model.authenticate(self._username.text(), self._password.text())
        if result is None:
            return
        self._authentication = result
        self.accept()

    def _on_view_model_changed(self, property_name: str) -> None:
        if property_name == "error_message":
            self._message.setText(self._view_model.error_message)
