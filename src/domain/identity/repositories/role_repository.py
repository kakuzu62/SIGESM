from __future__ import annotations

from abc import abstractmethod

from domain.contracts.repository import IRepository
from domain.identity.entities import Role
from shared.kernel.identity import Identity


class IRoleRepository(IRepository[Role, Identity]):
    """Repository contract for roles."""

    @abstractmethod
    def get_by_name(self, name: str) -> Role | None:
        """Return a role by name."""
        raise NotImplementedError
