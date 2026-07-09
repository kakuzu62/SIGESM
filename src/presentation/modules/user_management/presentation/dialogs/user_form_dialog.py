from __future__ import annotations

from PySide6.QtWidgets import QDialog, QFormLayout, QHBoxLayout, QLineEdit, QPushButton, QVBoxLayout

from presentation.modules.user_management.application.dto import CreateUserDTO, UpdateUserDTO


class UserFormDialog(QDialog):
    """Dialog for creating or editing a user."""

    def __init__(self, user_id: str | None = None, username: str = "", email: str = "") -> None:
        super().__init__()
        self._user_id = user_id
        self._username = QLineEdit(username)
        self._email = QLineEdit(email)
        self._password = QLineEdit()
        self._password.setEchoMode(QLineEdit.EchoMode.Password)
        self._build()

    def create_dto(self) -> CreateUserDTO:
        """Return create DTO."""
        return CreateUserDTO(
            username=self._username.text(),
            email=self._email.text(),
            password=self._password.text(),
        )

    def update_dto(self) -> UpdateUserDTO:
        """Return update DTO."""
        return UpdateUserDTO(
            user_id=self._user_id or "",
            username=self._username.text(),
            email=self._email.text(),
        )

    def _build(self) -> None:
        self.setWindowTitle("Usuario")
        form = QFormLayout()
        form.addRow("Usuario", self._username)
        form.addRow("Email", self._email)
        if self._user_id is None:
            form.addRow("Senha", self._password)
        save = QPushButton("Salvar")
        cancel = QPushButton("Cancelar")
        save.clicked.connect(self.accept)
        cancel.clicked.connect(self.reject)
        buttons = QHBoxLayout()
        buttons.addWidget(save)
        buttons.addWidget(cancel)
        layout = QVBoxLayout(self)
        layout.addLayout(form)
        layout.addLayout(buttons)
