from __future__ import annotations

from PySide6.QtWidgets import QFrame, QGridLayout, QLabel, QVBoxLayout, QWidget

from presentation.modules.dashboard.dashboard_view_model import DashboardViewModel


class DashboardView(QWidget):
    """Initial dashboard view with placeholder operational cards."""

    def __init__(self, view_model: DashboardViewModel | None = None) -> None:
        super().__init__()
        self._view_model = view_model or DashboardViewModel()
        layout = QVBoxLayout(self)
        title = QLabel("Dashboard")
        title.setObjectName("title")
        subtitle = QLabel("Visao inicial do SIGESM Enterprise")
        subtitle.setObjectName("subtitle")
        grid = QGridLayout()
        for index, metric in enumerate(self._view_model.metrics):
            grid.addWidget(self._card(metric.title, metric.value), index // 3, index % 3)
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addLayout(grid)
        layout.addStretch()

    @staticmethod
    def _card(title: str, value: str) -> QFrame:
        card = QFrame()
        card.setObjectName("card")
        layout = QVBoxLayout(card)
        label = QLabel(title)
        label.setObjectName("subtitle")
        metric = QLabel(value)
        layout.addWidget(label)
        layout.addWidget(metric)
        return card
