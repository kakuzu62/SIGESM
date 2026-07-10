from __future__ import annotations

from typing import Any

from PySide6.QtCore import QAbstractTableModel, QModelIndex, QPersistentModelIndex, Qt

from presentation.modules.user_management.application.queries.list_users import UserListItemDTO


class UserTableModel(QAbstractTableModel):
    """Qt table model for user listing."""

    _headers = ("Login", "Nome", "E-mail", "Status", "Perfis", "Ultimo acesso")
    _sort_fields = ("login", "name", "email", "status", "profiles", "last_access_at")

    def __init__(self) -> None:
        super().__init__()
        self._items: tuple[UserListItemDTO, ...] = ()

    def set_items(self, items: tuple[UserListItemDTO, ...]) -> None:
        """Replace table items."""
        self.beginResetModel()
        self._items = items
        self.endResetModel()

    def item_at(self, row: int) -> UserListItemDTO | None:
        """Return item at row."""
        if row < 0 or row >= len(self._items):
            return None
        return self._items[row]

    def sort_field(self, column: int) -> str:
        """Return query sort field for a column."""
        if column < 0 or column >= len(self._sort_fields):
            return "login"
        return self._sort_fields[column]

    def rowCount(  # noqa: N802
        self, parent: QModelIndex | QPersistentModelIndex | None = None
    ) -> int:
        """Return row count."""
        return 0 if parent is not None and parent.isValid() else len(self._items)

    def columnCount(  # noqa: N802
        self, parent: QModelIndex | QPersistentModelIndex | None = None
    ) -> int:
        """Return column count."""
        return 0 if parent is not None and parent.isValid() else len(self._headers)

    def data(
        self,
        index: QModelIndex | QPersistentModelIndex,
        role: int = Qt.ItemDataRole.DisplayRole,
    ) -> Any:
        """Return display data."""
        if not index.isValid() or role != Qt.ItemDataRole.DisplayRole:
            return None
        user = self._items[index.row()]
        values = (
            user.login,
            user.name,
            user.email,
            user.status,
            ", ".join(user.profiles),
            "" if user.last_access_at is None else user.last_access_at.strftime("%d/%m/%Y %H:%M"),
        )
        return values[index.column()]

    def headerData(  # noqa: N802
        self,
        section: int,
        orientation: Qt.Orientation,
        role: int = Qt.ItemDataRole.DisplayRole,
    ) -> Any:
        """Return header data."""
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return self._headers[section]
        return None
