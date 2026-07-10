from __future__ import annotations

from PySide6.QtCore import QModelIndex
from PySide6.QtWidgets import QLabel, QTableView, QVBoxLayout, QWidget

from presentation.framework.components import CrudToolbar
from presentation.modules.user_management.presentation.dialogs import UserFormDialog
from presentation.modules.user_management.presentation.models import UserTableModel
from presentation.modules.user_management.presentation.viewmodels import UserListViewModel
from presentation.modules.user_management.presentation.widgets import PaginationWidget, SearchBar


class UserListView(QWidget):
    """User listing screen."""

    def __init__(self, view_model: UserListViewModel) -> None:
        super().__init__()
        self._view_model = view_model
        self._table_model = UserTableModel()
        self._table = QTableView()
        self._message = QLabel("")
        self._pagination = PaginationWidget(self._view_model.change_page)
        self._build()
        self._view_model.subscribe(self._on_view_model_changed)
        self._view_model.load()
        self._refresh_table()

    def _build(self) -> None:
        title = QLabel("Usuarios")
        title.setObjectName("title")
        self._table.setModel(self._table_model)
        self._table.setSortingEnabled(False)
        self._table.horizontalHeader().sectionClicked.connect(self._sort_by_column)
        layout = QVBoxLayout(self)
        layout.addWidget(title)
        layout.addWidget(SearchBar(self._view_model.search))
        layout.addWidget(
            CrudToolbar(
                self._view_model.request_new_user,
                self._request_edit_selected,
                self._view_model.refresh,
            )
        )
        layout.addWidget(self._message)
        layout.addWidget(self._table)
        layout.addWidget(self._pagination)

    def _selected_user(self) -> int:
        index: QModelIndex = self._table.currentIndex()
        return index.row()

    def _request_edit_selected(self) -> None:
        self._view_model.request_edit_user(self._table_model.item_at(self._selected_user()))

    def _sort_by_column(self, column: int) -> None:
        self._view_model.sort(self._table_model.sort_field(column))

    def _refresh_table(self) -> None:
        self._table_model.set_items(self._view_model.users)
        self._pagination.update_state(self._view_model.page, self._view_model.total_pages)

    def _on_view_model_changed(self, property_name: str) -> None:
        if property_name == "users":
            self._refresh_table()
        elif property_name == "error_message":
            self._message.setText(self._view_model.error_message)
        elif property_name == "open_new_requested":
            UserFormDialog().exec()
        elif (
            property_name == "open_edit_requested"
            and self._view_model.open_edit_requested is not None
        ):
            UserFormDialog(self._view_model.open_edit_requested).exec()
