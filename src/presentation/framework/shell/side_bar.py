from __future__ import annotations

from collections.abc import Callable

from PySide6.QtWidgets import QFrame, QPushButton, QVBoxLayout

from presentation.framework.navigation import NavigationItem


class SideBar(QFrame):
    """Collapsible-ready module navigation bar."""

    def __init__(
        self,
        items: tuple[NavigationItem, ...],
        navigate: Callable[[str], None],
    ) -> None:
        super().__init__()
        self.setObjectName("sidebar")
        layout = QVBoxLayout(self)
        for item in items:
            button = QPushButton(item.title)
            button.clicked.connect(lambda _checked=False, key=item.key: navigate(key))
            layout.addWidget(button)
        layout.addStretch()
