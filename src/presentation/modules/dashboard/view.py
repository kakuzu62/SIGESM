from __future__ import annotations

from PySide6.QtWidgets import QFrame, QGridLayout, QLabel, QVBoxLayout, QWidget


class DashboardView(QWidget):
    """Initial dashboard view with placeholder operational cards."""

    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)
        title = QLabel("Dashboard")
        title.setObjectName("title")
        subtitle = QLabel("Visao inicial do SIGESM Enterprise")
        subtitle.setObjectName("subtitle")
        grid = QGridLayout()
        for index, label in enumerate(
            ("Militares", "Escalas", "Organizacoes", "Pendencias", "Auditoria")
        ):
            grid.addWidget(self._card(label), index // 3, index % 3)
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addLayout(grid)
        layout.addStretch()

    @staticmethod
    def _card(title: str) -> QFrame:
        card = QFrame()
        card.setObjectName("card")
        layout = QVBoxLayout(card)
        label = QLabel(title)
        label.setObjectName("subtitle")
        value = QLabel("Em preparacao")
        layout.addWidget(label)
        layout.addWidget(value)
        return card
