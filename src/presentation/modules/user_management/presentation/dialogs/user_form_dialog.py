from __future__ import annotations

from PySide6.QtWidgets import QDialog, QFormLayout, QLineEdit, QPushButton, QVBoxLayout

from presentation.modules.user_management.application.queries.list_users import UserListItemDTO


class UserFormDialog(QDialog):
    """Placeholder form dialog for the next user management STSs."""

    def __init__(self, user: UserListItemDTO | None = None) -> None:
        super().__init__()
        self._login = QLineEdit(user.login if user is not None else "")
        self._name = QLineEdit(user.name if user is not None else "")
        self._email = QLineEdit(user.email if user is not None else "")
        self._build(user is None)

    def _build(self, creating: bool) -> None:
        self.setWindowTitle("Novo usuario" if creating else "Editar usuario")
        form = QFormLayout()
        form.addRow("Login", self._login)
        form.addRow("Nome", self._name)
        form.addRow("E-mail", self._email)
        close_button = QPushButton("Fechar")
        close_button.clicked.connect(self.accept)
        layout = QVBoxLayout(self)
        layout.addLayout(form)
        layout.addWidget(close_button)
