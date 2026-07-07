from __future__ import annotations

from abc import abstractmethod

from domain.contracts.repository import IRepository
from domain.identity.entities import Permission
from domain.identity.value_objects import PermissionCode
from shared.kernel.identity import Identity


class IPermissionRepository(IRepository[Permission, Identity]):
    """Repository contract for permissions."""

    @abstractmethod
    def get_by_code(self, code: PermissionCode) -> Permission | None:
        """Return a permission by code."""
        raise NotImplementedError
