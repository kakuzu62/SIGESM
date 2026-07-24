from __future__ import annotations

from PySide6.QtWidgets import (
    QCheckBox,
    QDialog,
    QLabel,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
    QHBoxLayout,
)

from presentation.modules.user_management.presentation.viewmodels import UserRolesViewModel


class UserRolesDialog(QDialog):
    """Dialog used to manage roles assigned to a user."""

    def __init__(self, view_model: UserRolesViewModel) -> None:
        super().__init__()
        self._view_model = view_model
        self._general_error = QLabel("")
        self._roles_container = QWidget()
        self._roles_layout = QVBoxLayout(self._roles_container)
        self._checkboxes: dict[str, QCheckBox] = {}
        self._save_button = QPushButton("Salvar")
        self._cancel_button = QPushButton("Cancelar")
        self._build()
        self._connect()
        self._view_model.load()
        self._sync_state()

    def _build(self) -> None:
        self.setWindowTitle("Gerenciar perfis")
        self._general_error.setObjectName("errorMessage")
        target = QLabel(f"Usuario: {self._view_model.target_user_display_name}")
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self._roles_container)

        buttons = QHBoxLayout()
        buttons.addStretch()
        buttons.addWidget(self._save_button)
        buttons.addWidget(self._cancel_button)

        layout = QVBoxLayout(self)
        layout.addWidget(target)
        layout.addWidget(self._general_error)
        layout.addWidget(scroll)
        layout.addLayout(buttons)

    def _connect(self) -> None:
        self._cancel_button.clicked.connect(self.reject)
        self._save_button.clicked.connect(self._view_model.submit)
        self._view_model.roles_loaded.connect(self._render_roles)
        self._view_model.roles_updated.connect(self._on_operation_succeeded)
        self._view_model.update_failed.connect(self._on_operation_failed)
        self._view_model.subscribe(self._on_view_model_changed)

    def _render_roles(self) -> None:
        for checkbox in self._checkboxes.values():
            checkbox.setParent(None)
        self._checkboxes = {}
        selected = set(self._view_model.selected_role_ids)
        for role in self._view_model.available_roles:
            checkbox = QCheckBox(role.name)
            checkbox.setChecked(role.id in selected)
            checkbox.setEnabled(role.active)
            checkbox.toggled.connect(
                lambda checked, role_id=role.id: self._view_model.set_role_selected(
                    role_id, checked
                )
            )
            self._checkboxes[role.id] = checkbox
            self._roles_layout.addWidget(checkbox)
        self._roles_layout.addStretch()
        self._sync_state()

    def _on_view_model_changed(self, property_name: str) -> None:
        if property_name == "general_error":
            self._general_error.setText(self._view_model.general_error)
        elif property_name == "is_loading":
            self._set_loading(self._view_model.is_loading)
        elif property_name == "can_submit":
            self._save_button.setEnabled(self._view_model.can_submit)

    def _sync_state(self) -> None:
        self._save_button.setEnabled(self._view_model.can_submit)

    def _set_loading(self, is_loading: bool) -> None:
        for checkbox in self._checkboxes.values():
            checkbox.setEnabled(not is_loading)
        self._cancel_button.setEnabled(not is_loading)
        self._save_button.setEnabled(not is_loading and self._view_model.can_submit)

    def _on_operation_succeeded(self, _user: object) -> None:
        self.accept()

    def _on_operation_failed(self, message: str) -> None:
        self._general_error.setText(message)
