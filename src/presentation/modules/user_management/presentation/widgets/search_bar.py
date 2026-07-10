from __future__ import annotations

from collections.abc import Callable

from PySide6.QtWidgets import QHBoxLayout, QLineEdit, QPushButton, QWidget


class SearchBar(QWidget):
    """Search widget prepared for future debounce."""

    def __init__(self, on_search: Callable[[str], None]) -> None:
        super().__init__()
        self._on_search = on_search
        self._input = QLineEdit()
        self._input.setPlaceholderText("Pesquisar usuarios")
        self._input.textChanged.connect(self._on_search)
        button = QPushButton("Pesquisar")
        button.clicked.connect(self._search)
        layout = QHBoxLayout(self)
        layout.addWidget(self._input, stretch=1)
        layout.addWidget(button)

    def _search(self) -> None:
        self._on_search(self._input.text())
