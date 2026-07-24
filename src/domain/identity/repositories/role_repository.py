from __future__ import annotations

from abc import abstractmethod
from collections.abc import Sequence

from domain.contracts.repository import IRepository
from domain.identity.entities import Role
from shared.kernel.identity import Identity


class IRoleRepository(IRepository[Role, Identity]):
    """Repository contract for roles."""

    @abstractmethod
    def get_by_name(self, name: str) -> Role | None:
        """Return a role by name."""
        raise NotImplementedError

    @abstractmethod
    def get_by_ids(self, role_ids: Sequence[Identity]) -> tuple[Role, ...]:
        """Return roles matching the provided identities."""
        raise NotImplementedError

    @abstractmethod
    def list_active(self) -> tuple[Role, ...]:
        """Return active roles available for assignment."""
        raise NotImplementedError

    @abstractmethod
    def count_active_users_with_role(self, role_id: Identity) -> int:
        """Return active user count assigned to the role."""
        raise NotImplementedError
