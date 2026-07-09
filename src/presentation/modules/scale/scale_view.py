from __future__ import annotations

from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

from presentation.modules.scale.scale_view_model import ScaleViewModel


class ScaleView(QWidget):
    """Service scale module placeholder view."""

    def __init__(self, view_model: ScaleViewModel | None = None) -> None:
        super().__init__()
        self._view_model = view_model or ScaleViewModel()
        layout = QVBoxLayout(self)
        title = QLabel("Escalas")
        title.setObjectName("title")
        message = QLabel(self._view_model.status_message)
        layout.addWidget(title)
        layout.addWidget(message)
        layout.addStretch()
