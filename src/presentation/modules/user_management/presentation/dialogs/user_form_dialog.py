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

from presentation.modules.user_management.application.queries.list_users import UserListItemDTO
from presentation.modules.user_management.presentation.viewmodels import (
    CreateUserViewModel,
    EditUserViewModel,
)

UserFormViewModel = CreateUserViewModel | EditUserViewModel


class UserFormDialog(QDialog):
    """Dialog used to create a user or preview edit data."""

    def __init__(
        self,
        view_model: UserFormViewModel | None = None,
        user: UserListItemDTO | None = None,
    ) -> None:
        super().__init__()
        self._view_model = view_model
        self._creating = isinstance(view_model, CreateUserViewModel)
        self._editing = isinstance(view_model, EditUserViewModel)
        self._full_name = QLineEdit(self._initial_full_name(user))
        self._username = QLineEdit(self._initial_username(user))
        self._email = QLineEdit(self._initial_email(user))
        self._password = QLineEdit()
        self._password_confirmation = QLineEdit()
        self._general_error = QLabel("")
        self._field_errors: dict[str, QLabel] = {
            "full_name": QLabel(""),
            "username": QLabel(""),
            "email": QLabel(""),
            "password": QLabel(""),
            "password_confirmation": QLabel(""),
        }
        self._save_button = QPushButton("Salvar")
        self._cancel_button = QPushButton("Cancelar" if view_model is not None else "Fechar")
        self._build()
        self._connect()
        self._sync_state()

    def _build(self) -> None:
        self.setWindowTitle("Novo usuario" if self._creating else "Editar usuario")
        self._password.setEchoMode(QLineEdit.EchoMode.Password)
        self._password_confirmation.setEchoMode(QLineEdit.EchoMode.Password)
        self._general_error.setObjectName("errorMessage")

        form = QFormLayout()
        self._add_field(form, "Nome completo", self._full_name, "full_name")
        self._add_field(form, "Login", self._username, "username")
        self._add_field(form, "E-mail", self._email, "email")
        if self._creating:
            self._add_field(form, "Senha inicial", self._password, "password")
            self._add_field(
                form,
                "Confirmar senha",
                self._password_confirmation,
                "password_confirmation",
            )
        elif not self._editing:
            self._full_name.setReadOnly(True)
            self._username.setReadOnly(True)
            self._email.setReadOnly(True)
            self._save_button.setVisible(False)

        buttons = QHBoxLayout()
        buttons.addStretch()
        buttons.addWidget(self._save_button)
        buttons.addWidget(self._cancel_button)

        layout = QVBoxLayout(self)
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
        if self._view_model is None:
            return

        self._save_button.clicked.connect(self._view_model.submit)
        self._full_name.textChanged.connect(
            lambda value: self._view_model.update_input("full_name", value)
        )
        self._username.textChanged.connect(
            lambda value: self._view_model.update_input("username", value)
        )
        self._email.textChanged.connect(lambda value: self._view_model.update_input("email", value))
        if isinstance(self._view_model, CreateUserViewModel):
            self._password.textChanged.connect(
                lambda value: self._view_model.update_input("password", value)
            )
            self._password_confirmation.textChanged.connect(
                lambda value: self._view_model.update_input("password_confirmation", value)
            )
            self._view_model.user_created.connect(self._on_operation_succeeded)
            self._view_model.creation_failed.connect(self._on_operation_failed)
        elif isinstance(self._view_model, EditUserViewModel):
            self._view_model.user_updated.connect(self._on_operation_succeeded)
            self._view_model.update_failed.connect(self._on_operation_failed)
        self._view_model.subscribe(self._on_view_model_changed)

    def _sync_state(self) -> None:
        if self._view_model is None:
            return
        self._save_button.setEnabled(self._view_model.can_submit)

    def _on_view_model_changed(self, property_name: str) -> None:
        if self._view_model is None:
            return
        if property_name == "field_errors":
            self._render_field_errors()
        elif property_name == "general_error":
            self._general_error.setText(self._view_model.general_error)
        elif property_name == "is_loading":
            self._set_loading(self._view_model.is_loading)
        elif property_name == "can_submit":
            self._save_button.setEnabled(self._view_model.can_submit)
        elif property_name == "password":
            self._password.clear()
        elif property_name == "password_confirmation":
            self._password_confirmation.clear()

    def _render_field_errors(self) -> None:
        if self._view_model is None:
            return
        errors = self._view_model.field_errors
        for field_name, label in self._field_errors.items():
            label.setText(errors.get(field_name, ""))

    def _set_loading(self, is_loading: bool) -> None:
        self._full_name.setEnabled(not is_loading)
        self._username.setEnabled(not is_loading)
        self._email.setEnabled(not is_loading)
        self._password.setEnabled(not is_loading)
        self._password_confirmation.setEnabled(not is_loading)
        self._cancel_button.setEnabled(not is_loading)
        self._save_button.setEnabled(
            not is_loading and self._view_model is not None and self._view_model.can_submit
        )

    def _on_operation_succeeded(self, _user: object) -> None:
        self.accept()

    def _on_operation_failed(self, message: str) -> None:
        self._general_error.setText(message)

    def _initial_full_name(self, user: UserListItemDTO | None) -> str:
        if isinstance(self._view_model, EditUserViewModel):
            return self._view_model.full_name
        return user.name if user is not None else ""

    def _initial_username(self, user: UserListItemDTO | None) -> str:
        if isinstance(self._view_model, EditUserViewModel):
            return self._view_model.username
        return user.login if user is not None else ""

    def _initial_email(self, user: UserListItemDTO | None) -> str:
        if isinstance(self._view_model, EditUserViewModel):
            return self._view_model.email
        return user.email if user is not None else ""
