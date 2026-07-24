from __future__ import annotations

from PySide6.QtCore import Signal

from presentation.framework.mvvm import ViewModel
from presentation.modules.user_management.application import ResetPasswordService
from presentation.modules.user_management.application.commands.reset_password import (
    ResetPasswordCommand,
)
from presentation.modules.user_management.application.queries.list_users import UserListItemDTO


class ResetPasswordViewModel(ViewModel):
    """ViewModel responsible for administrator password reset."""

    password_reset = Signal(object)
    reset_failed = Signal(str)

    def __init__(
        self,
        actor_user_id: str,
        target_user: UserListItemDTO,
        service: ResetPasswordService,
    ) -> None:
        super().__init__()
        self._actor_user_id = actor_user_id
        self._target_user = target_user
        self._service = service
        self._new_password = ""
        self._confirm_password = ""
        self._field_errors: dict[str, str] = {}
        self._general_error = ""
        self._is_loading = False
        self._success = False

    @property
    def target_label(self) -> str:
        """Return safe target user label."""
        return f"{self._target_user.name} ({self._target_user.login})"

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
    def success(self) -> bool:
        """Return whether the last reset completed successfully."""
        return self._success

    @property
    def can_submit(self) -> bool:
        """Return whether password reset can be submitted."""
        return not self._is_loading and bool(self._new_password) and bool(self._confirm_password)

    def update_input(self, field_name: str, value: str) -> None:
        """Update one password input field without emitting the password."""
        if field_name == "new_password":
            self._new_password = value
        elif field_name == "confirm_password":
            self._confirm_password = value
        self._field_errors.pop(field_name, None)
        self.notify_property_changed("field_errors")
        self.notify_property_changed("can_submit")

    def submit(self) -> None:
        """Submit the password reset form."""
        if self._is_loading:
            return

        self._clear_messages()
        if not self._validate_input():
            self.reset_failed.emit(self._general_error)
            return

        self._set_loading(True)
        try:
            result = self._service.reset_password(
                ResetPasswordCommand(
                    actor_user_id=self._actor_user_id,
                    target_user_id=self._target_user.id,
                    new_password=self._new_password,
                )
            )
            if result.is_failure:
                self._apply_failure(result.error)
                self.reset_failed.emit(result.error)
                return

            self._success = True
            self._clear_passwords()
            self.notify_property_changed("success")
            self.password_reset.emit(result.value)
        finally:
            self._set_loading(False)

    def clear_sensitive_fields(self) -> None:
        """Clear password fields without touching non-sensitive state."""
        self._clear_passwords()

    def _validate_input(self) -> bool:
        if not self._new_password:
            self._field_errors["new_password"] = "Nova senha e obrigatoria."
        if not self._confirm_password:
            self._field_errors["confirm_password"] = "Confirmacao da senha e obrigatoria."
        elif self._new_password != self._confirm_password:
            self._field_errors["confirm_password"] = "A confirmacao da senha nao corresponde."

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
        self._success = False
        self.notify_property_changed("field_errors")
        self.notify_property_changed("general_error")
        self.notify_property_changed("success")

    def _apply_failure(self, message: str) -> None:
        self._general_error = message
        lowered = message.lower()
        if "password" in lowered or "senha" in lowered:
            self._field_errors["new_password"] = message
        self.notify_property_changed("field_errors")
        self.notify_property_changed("general_error")

    def _clear_passwords(self) -> None:
        self._new_password = ""
        self._confirm_password = ""
        self.notify_property_changed("new_password")
        self.notify_property_changed("confirm_password")
        self.notify_property_changed("can_submit")

    def _set_loading(self, is_loading: bool) -> None:
        self._is_loading = is_loading
        self.notify_property_changed("is_loading")
        self.notify_property_changed("can_submit")
