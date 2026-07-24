from __future__ import annotations

from collections.abc import Callable

from PySide6.QtWidgets import QHBoxLayout, QPushButton, QWidget


class CrudToolbar(QWidget):
    """Reusable CRUD toolbar."""

    def __init__(
        self,
        on_new: Callable[[], None],
        on_edit: Callable[[], None],
        on_refresh: Callable[[], None],
        on_change_status: Callable[[], None] | None = None,
        on_reset_password: Callable[[], None] | None = None,
        on_manage_roles: Callable[[], None] | None = None,
    ) -> None:
        super().__init__()
        layout = QHBoxLayout(self)
        new_button = QPushButton("Novo")
        edit_button = QPushButton("Editar")
        refresh_button = QPushButton("Atualizar")
        self._status_button = QPushButton("Ativar/Desativar")
        self._reset_password_button = QPushButton("Redefinir Senha")
        self._roles_button = QPushButton("Gerenciar Perfis")
        delete_button = QPushButton("Excluir")
        delete_button.setEnabled(False)
        new_button.clicked.connect(on_new)
        edit_button.clicked.connect(on_edit)
        refresh_button.clicked.connect(on_refresh)
        if on_change_status is not None:
            self._status_button.clicked.connect(on_change_status)
        self._status_button.setEnabled(on_change_status is not None)
        if on_reset_password is not None:
            self._reset_password_button.clicked.connect(on_reset_password)
        self._reset_password_button.setEnabled(on_reset_password is not None)
        if on_manage_roles is not None:
            self._roles_button.clicked.connect(on_manage_roles)
        self._roles_button.setEnabled(on_manage_roles is not None)
        layout.addWidget(new_button)
        layout.addWidget(edit_button)
        layout.addWidget(self._status_button)
        layout.addWidget(self._reset_password_button)
        layout.addWidget(self._roles_button)
        layout.addWidget(refresh_button)
        layout.addWidget(delete_button)
        layout.addStretch()

    def set_status_action(self, label: str, enabled: bool) -> None:
        """Update status action label and enabled state."""
        self._status_button.setText(label)
        self._status_button.setEnabled(enabled)

    def set_reset_password_action(self, enabled: bool) -> None:
        """Update reset password action enabled state."""
        self._reset_password_button.setEnabled(enabled)

    def set_roles_action(self, enabled: bool) -> None:
        """Update manage roles action enabled state."""
        self._roles_button.setEnabled(enabled)
