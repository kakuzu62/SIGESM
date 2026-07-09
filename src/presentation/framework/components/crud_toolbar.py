from __future__ import annotations

from collections.abc import Callable

from PySide6.QtWidgets import QHBoxLayout, QPushButton, QWidget


class CrudToolbar(QWidget):
    """Reusable CRUD toolbar."""

    def __init__(
        self,
        on_new: Callable[[], None],
        on_edit: Callable[[], None],
        on_activate: Callable[[], None],
        on_deactivate: Callable[[], None],
        on_reset_password: Callable[[], None],
        on_refresh: Callable[[], None],
    ) -> None:
        super().__init__()
        actions = (
            ("Novo", on_new),
            ("Editar", on_edit),
            ("Ativar", on_activate),
            ("Desativar", on_deactivate),
            ("Redefinir Senha", on_reset_password),
            ("Atualizar", on_refresh),
        )
        layout = QHBoxLayout(self)
        for label, callback in actions:
            button = QPushButton(label)
            button.clicked.connect(callback)
            layout.addWidget(button)
        layout.addStretch()
