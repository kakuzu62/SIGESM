"""Identity repository contracts."""

from domain.identity.repositories.permission_repository import IPermissionRepository
from domain.identity.repositories.role_repository import IRoleRepository
from domain.identity.repositories.user_repository import IUserRepository

__all__ = [
    "IPermissionRepository",
    "IRoleRepository",
    "IUserRepository",
]
