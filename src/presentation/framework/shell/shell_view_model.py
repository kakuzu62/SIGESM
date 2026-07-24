from __future__ import annotations

from application.identity.dto import AuthenticationDTO
from presentation.framework.mvvm import ViewModel


class ShellViewModel(ViewModel):
    """View model for the main desktop shell."""

    def __init__(self, authentication: AuthenticationDTO) -> None:
        super().__init__()
        self._authentication = authentication

    @property
    def user_label(self) -> str:
        """Return the authenticated user label."""
        return f"Usuario: {self._authentication.user_id}"

    @property
    def user_id(self) -> str:
        """Return the authenticated user identity."""
        return self._authentication.user_id
