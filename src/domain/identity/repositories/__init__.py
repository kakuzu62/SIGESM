"""Identity repository contracts."""

from domain.identity.repositories.authentication_attempt_repository import (
    IAuthenticationAttemptRepository,
)
from domain.identity.repositories.authentication_session_repository import (
    IAuthenticationSessionRepository,
)
from domain.identity.repositories.permission_repository import IPermissionRepository
from domain.identity.repositories.refresh_session_repository import IRefreshSessionRepository
from domain.identity.repositories.role_repository import IRoleRepository
from domain.identity.repositories.password_reset_repository import IPasswordResetRequestRepository
from domain.identity.repositories.user_repository import IUserRepository

__all__ = [
    "IAuthenticationAttemptRepository",
    "IAuthenticationSessionRepository",
    "IPermissionRepository",
    "IPasswordResetRequestRepository",
    "IRefreshSessionRepository",
    "IRoleRepository",
    "IUserRepository",
]
