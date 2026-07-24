from __future__ import annotations

from PySide6.QtCore import QModelIndex
from PySide6.QtWidgets import QLabel, QMessageBox, QTableView, QVBoxLayout, QWidget

from presentation.framework.components import CrudToolbar
from presentation.modules.user_management.application.queries.list_users import UserListItemDTO
from presentation.modules.user_management.presentation.dialogs import (
    ResetPasswordDialog,
    UserFormDialog,
    UserRolesDialog,
)
from presentation.modules.user_management.presentation.models import UserTableModel
from presentation.modules.user_management.presentation.viewmodels import (
    UserListViewModel,
)
from presentation.modules.user_management.presentation.widgets import PaginationWidget, SearchBar


class UserListView(QWidget):
    """User listing screen."""

    def __init__(self, view_model: UserListViewModel) -> None:
        super().__init__()
        self._view_model = view_model
        self._table_model = UserTableModel()
        self._table = QTableView()
        self._message = QLabel("")
        self._search_bar = SearchBar(self._view_model.search)
        self._status_view_model = self._view_model.change_status_view_model()
        self._toolbar = CrudToolbar(
            self._view_model.request_new_user,
            self._request_edit_selected,
            self._view_model.refresh,
            self._request_status_change_selected,
            self._request_reset_password_selected,
            self._request_manage_roles_selected,
        )
        self._pagination = PaginationWidget(self._view_model.change_page)
        self._build()
        self._view_model.subscribe(self._on_view_model_changed)
        self._status_view_model.subscribe(self._on_status_view_model_changed)
        self._view_model.new_user_requested.connect(self._open_new_dialog)
        self._view_model.edit_user_requested.connect(self._open_edit_dialog)
        self._view_model.reset_password_requested.connect(self._open_reset_password_dialog)
        self._view_model.manage_roles_requested.connect(self._open_user_roles_dialog)
        self._status_view_model.confirmation_requested.connect(self._confirm_status_change)
        self._status_view_model.status_changed.connect(self._view_model.handle_user_status_changed)
        self._status_view_model.status_change_failed.connect(self._show_status_error)
        self._view_model.load()
        self._refresh_table()

    def _build(self) -> None:
        title = QLabel("Usuarios")
        title.setObjectName("title")
        self._table.setModel(self._table_model)
        self._table.setSortingEnabled(False)
        self._table.selectionModel().currentRowChanged.connect(self._sync_selected_user)
        self._table.horizontalHeader().sectionClicked.connect(self._sort_by_column)
        layout = QVBoxLayout(self)
        layout.addWidget(title)
        layout.addWidget(self._search_bar)
        layout.addWidget(self._toolbar)
        layout.addWidget(self._message)
        layout.addWidget(self._table)
        layout.addWidget(self._pagination)

    def _selected_user(self) -> int:
        index: QModelIndex = self._table.currentIndex()
        return index.row()

    def _request_edit_selected(self) -> None:
        self._view_model.request_edit_user(self._table_model.item_at(self._selected_user()))

    def _request_status_change_selected(self) -> None:
        self._status_view_model.request_change_status(
            self._table_model.item_at(self._selected_user())
        )

    def _request_reset_password_selected(self) -> None:
        self._view_model.request_reset_password(self._table_model.item_at(self._selected_user()))

    def _request_manage_roles_selected(self) -> None:
        self._view_model.request_manage_roles(self._table_model.item_at(self._selected_user()))

    def _sort_by_column(self, column: int) -> None:
        self._view_model.sort(self._table_model.sort_field(column))

    def _refresh_table(self) -> None:
        self._table_model.set_items(self._view_model.users)
        self._pagination.update_state(self._view_model.page, self._view_model.total_pages)
        self._status_view_model.select_user(self._table_model.item_at(self._selected_user()))
        self._sync_status_action()

    def _on_view_model_changed(self, property_name: str) -> None:
        if property_name == "users":
            self._refresh_table()
        elif property_name == "error_message":
            self._message.setText(self._view_model.error_message)
        elif property_name == "is_loading":
            self._set_loading(self._view_model.is_loading)

    def _set_loading(self, is_loading: bool) -> None:
        self._search_bar.setEnabled(not is_loading)
        self._toolbar.setEnabled(not is_loading)
        self._pagination.setEnabled(not is_loading)
        self._sync_status_action()

    def _open_new_dialog(self) -> None:
        create_view_model = self._view_model.create_user_view_model()
        create_view_model.user_created.connect(self._view_model.handle_user_created)
        UserFormDialog(create_view_model).exec()

    def _open_edit_dialog(self, user: object) -> None:
        if isinstance(user, UserListItemDTO):
            edit_view_model = self._view_model.edit_user_view_model(user)
            edit_view_model.user_updated.connect(self._view_model.handle_user_updated)
            UserFormDialog(edit_view_model).exec()

    def _sync_selected_user(
        self,
        current: QModelIndex | None = None,
        previous: QModelIndex | None = None,
    ) -> None:
        _ = (current, previous)
        self._status_view_model.select_user(self._table_model.item_at(self._selected_user()))
        self._sync_status_action()

    def _on_status_view_model_changed(self, property_name: str) -> None:
        if property_name in {"selected_user", "can_change_status", "is_loading"}:
            self._sync_status_action()
        elif property_name == "general_error":
            self._message.setText(self._status_view_model.general_error)

    def _sync_status_action(self) -> None:
        user = self._status_view_model.selected_user
        label = "Ativar" if user is not None and user.status == "Inativo" else "Desativar"
        enabled = self._status_view_model.can_change_status and not self._view_model.is_loading
        self._toolbar.set_status_action(label, enabled)
        self._toolbar.set_reset_password_action(enabled)
        self._toolbar.set_roles_action(enabled)

    def _confirm_status_change(self, message: str) -> None:
        answer = QMessageBox.question(
            self,
            "Confirmar alteracao",
            message,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if answer == QMessageBox.StandardButton.Yes:
            self._status_view_model.confirm_change_status()
        else:
            self._status_view_model.cancel_change_status()

    def _show_status_error(self, message: str) -> None:
        self._message.setText(message)

    def _open_reset_password_dialog(self, user: object) -> None:
        if isinstance(user, UserListItemDTO):
            reset_view_model = self._view_model.reset_password_view_model(user)
            reset_view_model.password_reset.connect(self._view_model.handle_password_reset)
            ResetPasswordDialog(reset_view_model).exec()

    def _open_user_roles_dialog(self, user: object) -> None:
        if isinstance(user, UserListItemDTO):
            roles_view_model = self._view_model.user_roles_view_model(user)
            roles_view_model.roles_updated.connect(self._view_model.handle_roles_updated)
            UserRolesDialog(roles_view_model).exec()
