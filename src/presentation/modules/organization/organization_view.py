from __future__ import annotations

from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

from presentation.modules.organization.organization_view_model import OrganizationViewModel


class OrganizationView(QWidget):
    """Organization module placeholder view."""

    def __init__(self, view_model: OrganizationViewModel | None = None) -> None:
        super().__init__()
        self._view_model = view_model or OrganizationViewModel()
        layout = QVBoxLayout(self)
        title = QLabel("Organizacao Militar")
        title.setObjectName("title")
        message = QLabel(self._view_model.status_message)
        layout.addWidget(title)
        layout.addWidget(message)
        layout.addStretch()
