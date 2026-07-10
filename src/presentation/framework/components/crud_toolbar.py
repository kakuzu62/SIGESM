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
    ) -> None:
        super().__init__()
        layout = QHBoxLayout(self)
        new_button = QPushButton("Novo")
        edit_button = QPushButton("Editar")
        refresh_button = QPushButton("Atualizar")
        delete_button = QPushButton("Excluir")
        delete_button.setEnabled(False)
        new_button.clicked.connect(on_new)
        edit_button.clicked.connect(on_edit)
        refresh_button.clicked.connect(on_refresh)
        layout.addWidget(new_button)
        layout.addWidget(edit_button)
        layout.addWidget(refresh_button)
        layout.addWidget(delete_button)
        layout.addStretch()
