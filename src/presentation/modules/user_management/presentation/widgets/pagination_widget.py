from __future__ import annotations

from collections.abc import Callable

from PySide6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QWidget


class PaginationWidget(QWidget):
    """Pagination widget for list screens."""

    def __init__(self, on_page_changed: Callable[[int], None]) -> None:
        super().__init__()
        self._on_page_changed = on_page_changed
        self._page = 1
        self._total_pages = 1
        self._label = QLabel("Pagina 1/1")
        first = QPushButton("Primeira")
        previous = QPushButton("Anterior")
        next_button = QPushButton("Proxima")
        last = QPushButton("Ultima")
        first.clicked.connect(lambda: self._on_page_changed(1))
        previous.clicked.connect(self._previous)
        next_button.clicked.connect(self._next)
        last.clicked.connect(self._last)
        layout = QHBoxLayout(self)
        layout.addWidget(first)
        layout.addWidget(previous)
        layout.addWidget(self._label)
        layout.addWidget(next_button)
        layout.addWidget(last)
        layout.addStretch()

    def update_state(self, page: int, total_pages: int) -> None:
        """Update pagination state."""
        self._page = page
        self._total_pages = max(total_pages, 1)
        self._label.setText(f"Pagina {self._page}/{self._total_pages}")

    def _previous(self) -> None:
        if self._page > 1:
            self._on_page_changed(self._page - 1)

    def _next(self) -> None:
        if self._page < self._total_pages:
            self._on_page_changed(self._page + 1)

    def _last(self) -> None:
        self._on_page_changed(self._total_pages)
