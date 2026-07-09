from __future__ import annotations

from collections.abc import Callable

from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton


class HeaderBar(QFrame):
    """Top bar for the SIGESM desktop shell."""

    def __init__(
        self,
        user_label: str,
        toggle_theme: Callable[[], None],
        close_application: Callable[[], None],
    ) -> None:
        super().__init__()
        self.setObjectName("header")
        layout = QHBoxLayout(self)
        title = QLabel("SIGESM Enterprise")
        title.setObjectName("title")
        user = QLabel(user_label)
        theme = QPushButton("Alternar tema")
        theme.clicked.connect(toggle_theme)
        exit_button = QPushButton("Sair")
        exit_button.clicked.connect(close_application)
        layout.addWidget(title)
        layout.addStretch()
        layout.addWidget(user)
        layout.addWidget(theme)
        layout.addWidget(exit_button)
