from __future__ import annotations

from application.identity.dto import AuthenticationDTO
from presentation.framework.controllers import LoginController
from presentation.framework.viewmodels.base import ObservableViewModel


class LoginViewModel(ObservableViewModel):
    """View model for the login dialog."""

    def __init__(self, controller: LoginController) -> None:
        super().__init__()
        self._controller = controller
        self._error_message = ""

    @property
    def error_message(self) -> str:
        """Return current login error message."""
        return self._error_message

    def authenticate(self, username: str, password: str) -> AuthenticationDTO | None:
        """Authenticate and expose a user-friendly error on failure."""
        try:
            self._error_message = ""
            result = self._controller.authenticate(username, password)
            self.notify_changed("error_message")
            return result
        except Exception:
            self._error_message = "Usuario ou senha invalidos."
            self.notify_changed("error_message")
            return None
