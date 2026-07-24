from __future__ import annotations

from PySide6.QtWidgets import (
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)

from presentation.modules.user_management.presentation.viewmodels import ResetPasswordViewModel


class ResetPasswordDialog(QDialog):
    """Dialog used by administrators to reset a user's password."""

    def __init__(self, view_model: ResetPasswordViewModel) -> None:
        super().__init__()
        self._view_model = view_model
        self._new_password = QLineEdit()
        self._confirm_password = QLineEdit()
        self._general_error = QLabel("")
        self._field_errors: dict[str, QLabel] = {
            "new_password": QLabel(""),
            "confirm_password": QLabel(""),
        }
        self._save_button = QPushButton("Redefinir")
        self._cancel_button = QPushButton("Cancelar")
        self._build()
        self._connect()
        self._sync_state()

    def reject(self) -> None:
        """Close the dialog and clear password inputs."""
        self._new_password.clear()
        self._confirm_password.clear()
        self._view_model.clear_sensitive_fields()
        super().reject()

    def _build(self) -> None:
        self.setWindowTitle("Redefinir senha")
        self._new_password.setEchoMode(QLineEdit.EchoMode.Password)
        self._confirm_password.setEchoMode(QLineEdit.EchoMode.Password)
        self._general_error.setObjectName("errorMessage")

        target = QLabel(f"Usuario: {self._view_model.target_label}")
        form = QFormLayout()
        self._add_field(form, "Nova senha", self._new_password, "new_password")
        self._add_field(form, "Confirmar senha", self._confirm_password, "confirm_password")

        buttons = QHBoxLayout()
        buttons.addStretch()
        buttons.addWidget(self._save_button)
        buttons.addWidget(self._cancel_button)

        layout = QVBoxLayout(self)
        layout.addWidget(target)
        layout.addWidget(self._general_error)
        layout.addLayout(form)
        layout.addLayout(buttons)

    def _add_field(
        self,
        form: QFormLayout,
        label: str,
        input_field: QLineEdit,
        error_key: str,
    ) -> None:
        container = QVBoxLayout()
        error = self._field_errors[error_key]
        error.setObjectName("fieldError")
        container.addWidget(input_field)
        container.addWidget(error)
        form.addRow(label, container)

    def _connect(self) -> None:
        self._cancel_button.clicked.connect(self.reject)
        self._save_button.clicked.connect(self._view_model.submit)
        self._new_password.textChanged.connect(
            lambda value: self._view_model.update_input("new_password", value)
        )
        self._confirm_password.textChanged.connect(
            lambda value: self._view_model.update_input("confirm_password", value)
        )
        self._view_model.password_reset.connect(self._on_operation_succeeded)
        self._view_model.reset_failed.connect(self._on_operation_failed)
        self._view_model.subscribe(self._on_view_model_changed)

    def _sync_state(self) -> None:
        self._save_button.setEnabled(self._view_model.can_submit)

    def _on_view_model_changed(self, property_name: str) -> None:
        if property_name == "field_errors":
            self._render_field_errors()
        elif property_name == "general_error":
            self._general_error.setText(self._view_model.general_error)
        elif property_name == "is_loading":
            self._set_loading(self._view_model.is_loading)
        elif property_name == "can_submit":
            self._save_button.setEnabled(self._view_model.can_submit)
        elif property_name == "new_password":
            self._new_password.clear()
        elif property_name == "confirm_password":
            self._confirm_password.clear()

    def _render_field_errors(self) -> None:
        errors = self._view_model.field_errors
        for field_name, label in self._field_errors.items():
            label.setText(errors.get(field_name, ""))

    def _set_loading(self, is_loading: bool) -> None:
        self._new_password.setEnabled(not is_loading)
        self._confirm_password.setEnabled(not is_loading)
        self._cancel_button.setEnabled(not is_loading)
        self._save_button.setEnabled(not is_loading and self._view_model.can_submit)

    def _on_operation_succeeded(self, _user: object) -> None:
        self.accept()

    def _on_operation_failed(self, message: str) -> None:
        self._general_error.setText(message)
