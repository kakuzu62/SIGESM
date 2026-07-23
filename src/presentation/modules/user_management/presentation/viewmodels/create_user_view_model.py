from __future__ import annotations

from PySide6.QtCore import Signal

from presentation.framework.mvvm import ViewModel
from presentation.modules.user_management.application import CreateUserService
from presentation.modules.user_management.application.commands.create_user import (
    CreateUserCommand,
)
from presentation.modules.user_management.presentation.inputs import CreateUserInput


class CreateUserViewModel(ViewModel):
    """ViewModel responsible for the create user dialog."""

    user_created = Signal(object)
    creation_failed = Signal(str)

    def __init__(self, service: CreateUserService) -> None:
        super().__init__()
        self._service = service
        self._full_name = ""
        self._username = ""
        self._email = ""
        self._password = ""
        self._password_confirmation = ""
        self._field_errors: dict[str, str] = {}
        self._general_error = ""
        self._is_loading = False

    @property
    def full_name(self) -> str:
        """Return full name input."""
        return self._full_name

    @property
    def username(self) -> str:
        """Return username input."""
        return self._username

    @property
    def email(self) -> str:
        """Return email input."""
        return self._email

    @property
    def field_errors(self) -> dict[str, str]:
        """Return field validation messages."""
        return dict(self._field_errors)

    @property
    def general_error(self) -> str:
        """Return the general form error."""
        return self._general_error

    @property
    def is_loading(self) -> bool:
        """Return whether the form is submitting."""
        return self._is_loading

    @property
    def can_submit(self) -> bool:
        """Return whether the form currently has the minimum data to submit."""
        return (
            not self._is_loading
            and bool(self._full_name.strip())
            and bool(self._username.strip())
            and bool(self._email.strip())
            and bool(self._password)
            and bool(self._password_confirmation)
        )

    def update_input(self, field_name: str, value: str) -> None:
        """Update one form input field."""
        if field_name == "full_name":
            self._full_name = value
        elif field_name == "username":
            self._username = value
        elif field_name == "email":
            self._email = value
        elif field_name == "password":
            self._password = value
        elif field_name == "password_confirmation":
            self._password_confirmation = value
        self._field_errors.pop(field_name, None)
        self.notify_property_changed(field_name)
        self.notify_property_changed("field_errors")
        self.notify_property_changed("can_submit")

    def submit(self) -> None:
        """Submit the user creation form."""
        if self._is_loading:
            return

        self._clear_messages()
        input_model = CreateUserInput(
            full_name=self._full_name,
            username=self._username,
            email=self._email,
            password=self._password,
            password_confirmation=self._password_confirmation,
        )
        if not self._validate_input(input_model):
            self.creation_failed.emit(self._general_error)
            return

        self._set_loading(True)
        try:
            result = self._service.create_user(
                CreateUserCommand(
                    full_name=input_model.full_name,
                    username=input_model.username,
                    email=input_model.email,
                    password=input_model.password,
                )
            )
            if result.is_failure:
                self._apply_application_failure(result.error)
                self.creation_failed.emit(result.error)
                return

            self._clear_passwords()
            self.user_created.emit(result.value)
        finally:
            self._set_loading(False)

    def _validate_input(self, input_model: CreateUserInput) -> bool:
        if not input_model.full_name.strip():
            self._field_errors["full_name"] = "Nome completo e obrigatorio."
        if not input_model.username.strip():
            self._field_errors["username"] = "Login e obrigatorio."
        if not input_model.email.strip():
            self._field_errors["email"] = "E-mail e obrigatorio."
        if not input_model.password:
            self._field_errors["password"] = "Senha inicial e obrigatoria."
        if not input_model.password_confirmation:
            self._field_errors["password_confirmation"] = "Confirme a senha."
        if input_model.password and input_model.password != input_model.password_confirmation:
            self._field_errors["password_confirmation"] = "A confirmacao da senha nao corresponde."

        if self._field_errors:
            self._general_error = "Corrija os campos destacados."
            self.notify_property_changed("field_errors")
            self.notify_property_changed("general_error")
            self.notify_property_changed("can_submit")
            return False
        return True

    def _clear_messages(self) -> None:
        self._field_errors = {}
        self._general_error = ""
        self.notify_property_changed("field_errors")
        self.notify_property_changed("general_error")

    def _apply_application_failure(self, message: str) -> None:
        self._general_error = message
        if "login" in message.lower():
            self._field_errors["username"] = message
        elif "e-mail" in message.lower() or "email" in message.lower():
            self._field_errors["email"] = message
        elif "password" in message.lower() or "senha" in message.lower():
            self._field_errors["password"] = message
        self.notify_property_changed("field_errors")
        self.notify_property_changed("general_error")

    def _clear_passwords(self) -> None:
        self._password = ""
        self._password_confirmation = ""
        self.notify_property_changed("password")
        self.notify_property_changed("password_confirmation")
        self.notify_property_changed("can_submit")

    def _set_loading(self, is_loading: bool) -> None:
        self._is_loading = is_loading
        self.notify_property_changed("is_loading")
        self.notify_property_changed("can_submit")
