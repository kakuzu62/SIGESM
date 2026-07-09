from __future__ import annotations

from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

from presentation.modules.settings.settings_view_model import SettingsViewModel


class SettingsView(QWidget):
    """Settings module placeholder view."""

    def __init__(self, view_model: SettingsViewModel | None = None) -> None:
        super().__init__()
        self._view_model = view_model or SettingsViewModel()
        layout = QVBoxLayout(self)
        title = QLabel("Configuracoes")
        title.setObjectName("title")
        message = QLabel(self._view_model.status_message)
        layout.addWidget(title)
        layout.addWidget(message)
        layout.addStretch()
