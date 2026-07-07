"""Identity domain events."""

from domain.identity.events.login_failed import LoginFailed
from domain.identity.events.password_changed import PasswordChanged
from domain.identity.events.user_activated import UserActivated
from domain.identity.events.user_created import UserCreated
from domain.identity.events.user_deactivated import UserDeactivated

__all__ = [
    "LoginFailed",
    "PasswordChanged",
    "UserActivated",
    "UserCreated",
    "UserDeactivated",
]
