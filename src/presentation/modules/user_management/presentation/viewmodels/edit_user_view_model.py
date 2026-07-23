from __future__ import annotations

from PySide6.QtCore import Signal

from presentation.framework.mvvm import ViewModel
from presentation.modules.user_management.application import EditUserService
from presentation.modules.user_management.application.commands.update_user import (
    UpdateUserCommand,
)
from presentation.modules.user_management.application.queries.list_users import UserListItemDTO
from presentation.modules.user_management.presentation.inputs import EditUserInput


class EditUserViewModel(ViewModel):
    """ViewModel responsible for the edit user dialog."""

    user_updated = Signal(object)
    update_failed = Signal(str)

    def __init__(self, user: UserListItemDTO, service: EditUserService) -> None:
        super().__init__()
        self._service = service
        self._initial = EditUserInput(
            user_id=user.id,
            full_name=user.name,
            username=user.login,
            email=user.email,
        )
        self._user_id = self._initial.user_id
        self._full_name = self._initial.full_name
        self._username = self._initial.username
        self._email = self._initial.email
        self._field_errors: dict[str, str] = {}
        self._general_error = ""
        self._is_loading = False

    @property
    def user_id(self) -> str:
        """Return the immutable user identity."""
        return self._user_id

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
    def has_changes(self) -> bool:
        """Return whether editable fields differ from the initial DTO."""
        return (
            self._full_name != self._initial.full_name
            or self._username != self._initial.username
            or self._email != self._initial.email
        )

    @property
    def can_submit(self) -> bool:
        """Return whether the edit form can be submitted."""
        return (
            not self._is_loading
            and self.has_changes
            and bool(self._full_name.strip())
            and bool(self._username.strip())
            and bool(self._email.strip())
        )

    def update_input(self, field_name: str, value: str) -> None:
        """Update one form input field."""
        if field_name == "full_name":
            self._full_name = value
        elif field_name == "username":
            self._username = value
        elif field_name == "email":
            self._email = value
        self._field_errors.pop(field_name, None)
        self.notify_property_changed(field_name)
        self.notify_property_changed("field_errors")
        self.notify_property_changed("has_changes")
        self.notify_property_changed("can_submit")

    def submit(self) -> None:
        """Submit the user editing form."""
        if self._is_loading or not self.has_changes:
            return

        self._clear_messages()
        input_model = EditUserInput(
            user_id=self._user_id,
            full_name=self._full_name,
            username=self._username,
            email=self._email,
        )
        if not self._validate_input(input_model):
            self.update_failed.emit(self._general_error)
            return

        self._set_loading(True)
        try:
            result = self._service.update_user(
                UpdateUserCommand(
                    user_id=input_model.user_id,
                    full_name=input_model.full_name,
                    username=input_model.username,
                    email=input_model.email,
                )
            )
            if result.is_failure:
                self._apply_application_failure(result.error)
                self.update_failed.emit(result.error)
                return

            self.user_updated.emit(result.value)
        finally:
            self._set_loading(False)

    def _validate_input(self, input_model: EditUserInput) -> bool:
        if not input_model.full_name.strip():
            self._field_errors["full_name"] = "Nome completo e obrigatorio."
        if not input_model.username.strip():
            self._field_errors["username"] = "Login e obrigatorio."
        if not input_model.email.strip():
            self._field_errors["email"] = "E-mail e obrigatorio."

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
        self.notify_property_changed("field_errors")
        self.notify_property_changed("general_error")

    def _set_loading(self, is_loading: bool) -> None:
        self._is_loading = is_loading
        self.notify_property_changed("is_loading")
        self.notify_property_changed("can_submit")
