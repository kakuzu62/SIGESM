from __future__ import annotations

from collections.abc import Callable

from PySide6.QtWidgets import QHBoxLayout, QLineEdit, QPushButton, QWidget


class SearchBar(QWidget):
    """Reusable search bar."""

    def __init__(self, on_search: Callable[[str], None]) -> None:
        super().__init__()
        self._on_search = on_search
        self._input = QLineEdit()
        self._input.setPlaceholderText("Pesquisar")
        button = QPushButton("Pesquisar")
        button.clicked.connect(self._search)
        layout = QHBoxLayout(self)
        layout.addWidget(self._input, stretch=1)
        layout.addWidget(button)

    @property
    def text(self) -> str:
        """Return current search text."""
        return self._input.text()

    def _search(self) -> None:
        self._on_search(self._input.text())
