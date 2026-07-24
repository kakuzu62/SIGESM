from __future__ import annotations

from PySide6.QtCore import Signal

from presentation.framework.mvvm import ViewModel
from presentation.modules.user_management.application import ChangeUserActiveStatusService
from presentation.modules.user_management.application.commands.change_user_status import (
    ChangeUserActiveStatusCommand,
)
from presentation.modules.user_management.application.queries.list_users import UserListItemDTO


class ChangeUserActiveStatusViewModel(ViewModel):
    """ViewModel responsible for requesting and executing user status changes."""

    confirmation_requested = Signal(str)
    status_changed = Signal(object)
    status_change_failed = Signal(str)

    def __init__(
        self,
        actor_user_id: str,
        service: ChangeUserActiveStatusService,
    ) -> None:
        super().__init__()
        self._actor_user_id = actor_user_id
        self._service = service
        self._selected_user: UserListItemDTO | None = None
        self._is_loading = False
        self._general_error = ""
        self._pending_user: UserListItemDTO | None = None
        self._pending_state: bool | None = None

    @property
    def selected_user(self) -> UserListItemDTO | None:
        """Return the selected user."""
        return self._selected_user

    @property
    def is_loading(self) -> bool:
        """Return whether a status change is running."""
        return self._is_loading

    @property
    def can_change_status(self) -> bool:
        """Return whether a status change can be requested."""
        return self._selected_user is not None and not self._is_loading

    @property
    def confirmation_message(self) -> str:
        """Return the confirmation message for the selected user."""
        if self._selected_user is None:
            return ""
        if self._is_active(self._selected_user):
            return (
                f"Deseja desativar o usuario {self._selected_user.name}/"
                f"{self._selected_user.login}? Ele nao podera acessar o sistema "
                "enquanto estiver inativo."
            )
        return (
            f"Deseja ativar o usuario {self._selected_user.name}/"
            f"{self._selected_user.login}? Ele podera voltar a acessar o sistema."
        )

    @property
    def general_error(self) -> str:
        """Return the current status change error."""
        return self._general_error

    def select_user(self, user: UserListItemDTO | None) -> None:
        """Select a user for status change actions."""
        self._selected_user = user
        self._pending_user = None
        self._pending_state = None
        self._general_error = ""
        self.notify_property_changed("selected_user")
        self.notify_property_changed("can_change_status")
        self.notify_property_changed("confirmation_message")
        self.notify_property_changed("general_error")

    def request_change_status(self, user: UserListItemDTO | None = None) -> None:
        """Request confirmation for the selected user's status change."""
        if self._is_loading:
            return
        if user is not None:
            self.select_user(user)
        if self._selected_user is None:
            return

        self._pending_user = self._selected_user
        self._pending_state = not self._is_active(self._selected_user)
        self.confirmation_requested.emit(self.confirmation_message)

    def cancel_change_status(self) -> None:
        """Cancel a pending status change without calling the application layer."""
        self._pending_user = None
        self._pending_state = None

    def confirm_change_status(self) -> None:
        """Execute a confirmed status change."""
        if self._is_loading or self._pending_user is None or self._pending_state is None:
            return

        pending_user = self._pending_user
        pending_state = self._pending_state
        self._pending_user = None
        self._pending_state = None
        self._general_error = ""
        self.notify_property_changed("general_error")
        self._set_loading(True)
        try:
            result = self._service.change_status(
                ChangeUserActiveStatusCommand(
                    actor_user_id=self._actor_user_id,
                    target_user_id=pending_user.id,
                    is_active=pending_state,
                )
            )
            if result.is_failure:
                self._general_error = result.error
                self.notify_property_changed("general_error")
                self.status_change_failed.emit(result.error)
                return

            self.status_changed.emit(result.value)
        finally:
            self._set_loading(False)

    def _set_loading(self, is_loading: bool) -> None:
        self._is_loading = is_loading
        self.notify_property_changed("is_loading")
        self.notify_property_changed("can_change_status")

    @staticmethod
    def _is_active(user: UserListItemDTO) -> bool:
        return user.status.strip().lower() == "ativo"
