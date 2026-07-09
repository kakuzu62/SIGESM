from __future__ import annotations

from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

from presentation.modules.military.military_view_model import MilitaryViewModel


class MilitaryView(QWidget):
    """Military module placeholder view."""

    def __init__(self, view_model: MilitaryViewModel | None = None) -> None:
        super().__init__()
        self._view_model = view_model or MilitaryViewModel()
        layout = QVBoxLayout(self)
        title = QLabel("Cadastro de Militares")
        title.setObjectName("title")
        message = QLabel(self._view_model.status_message)
        layout.addWidget(title)
        layout.addWidget(message)
        layout.addStretch()
