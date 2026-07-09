from __future__ import annotations

from PySide6.QtWidgets import (
    QDialog,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from presentation.framework.components import (
    ConfirmationDialog,
    CrudToolbar,
    FilterPanel,
    PaginationWidget,
    SearchBar,
)
from presentation.modules.user_management.application.dto import UserListItemDTO
from presentation.modules.user_management.presentation.dialogs import (
    ResetPasswordDialog,
    UserFormDialog,
)
from presentation.modules.user_management.presentation.viewmodels import UserViewModel


class UserListView(QWidget):
    """User management list view."""

    def __init__(self, view_model: UserViewModel) -> None:
        super().__init__()
        self._view_model = view_model
        self._table = QTableWidget(0, 5)
        self._message = QLabel("")
        self._pagination = PaginationWidget(self._view_model.go_to_page)
        self._confirmation = ConfirmationDialog()
        self._build()
        self._view_model.subscribe(self._on_view_model_changed)
        self._view_model.load()
        self._refresh_table()

    def _build(self) -> None:
        title = QLabel("Gestao de Usuarios")
        title.setObjectName("title")
        self._table.setHorizontalHeaderLabels(
            ["Usuario", "Email", "Status", "Perfis", "Atualizado"]
        )
        toolbar = CrudToolbar(
            self._new_user,
            self._edit_user,
            self._activate_user,
            self._deactivate_user,
            self._reset_password,
            self._view_model.load,
        )
        layout = QVBoxLayout(self)
        layout.addWidget(title)
        layout.addWidget(SearchBar(self._view_model.search))
        layout.addWidget(FilterPanel(self._view_model.filter_status))
        layout.addWidget(toolbar)
        layout.addWidget(self._message)
        layout.addWidget(self._table)
        layout.addWidget(self._pagination)

    def _refresh_table(self) -> None:
        users = self._view_model.users
        self._table.setRowCount(len(users))
        for row, user in enumerate(users):
            values = (
                user.username,
                user.email,
                "Ativo" if user.active else "Inativo",
                ", ".join(user.roles),
                user.updated_at.strftime("%d/%m/%Y %H:%M"),
            )
            for column, value in enumerate(values):
                item = QTableWidgetItem(value)
                item.setData(256, user.id)
                self._table.setItem(row, column, item)
        self._pagination.update_state(self._view_model.page.page, self._view_model.page.total_pages)

    def _selected_user(self) -> UserListItemDTO | None:
        row = self._table.currentRow()
        if row < 0 or row >= len(self._view_model.users):
            return None
        return self._view_model.users[row]

    def _new_user(self) -> None:
        dialog = UserFormDialog()
        if dialog.exec() == QDialog.DialogCode.Accepted and self._view_model.create_user(
            dialog.create_dto()
        ):
            self._refresh_table()

    def _edit_user(self) -> None:
        user = self._selected_user()
        if user is None:
            return
        dialog = UserFormDialog(user.id, user.username, user.email)
        if dialog.exec() == QDialog.DialogCode.Accepted and self._view_model.update_user(
            dialog.update_dto()
        ):
            self._refresh_table()

    def _activate_user(self) -> None:
        user = self._selected_user()
        if user is not None and self._view_model.activate_user(user.id):
            self._refresh_table()

    def _deactivate_user(self) -> None:
        user = self._selected_user()
        if user is None:
            return
        if self._confirmation.confirm(self, "Desativar usuario", "Confirmar desativacao?"):
            if self._view_model.deactivate_user(user.id):
                self._refresh_table()

    def _reset_password(self) -> None:
        user = self._selected_user()
        if user is None:
            return
        dialog = ResetPasswordDialog()
        if dialog.exec() == QDialog.DialogCode.Accepted and self._view_model.reset_password(
            user.id, dialog.password
        ):
            self._refresh_table()

    def _on_view_model_changed(self, property_name: str) -> None:
        if property_name == "users":
            self._refresh_table()
        if property_name == "error_message":
            self._message.setText(self._view_model.error_message)
        if property_name == "success_message":
            self._message.setText(self._view_model.success_message)
