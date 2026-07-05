from __future__ import annotations

from abc import abstractmethod

from domain.contracts.repository import IRepository
from domain.organization.entities import Organization
from domain.organization.value_objects import OrganizationCode
from shared.kernel.identity import Identity


class IOrganizationRepository(IRepository[Organization, Identity]):
    """Repository contract for organization aggregates."""

    @abstractmethod
    def get_by_code(self, code: OrganizationCode) -> Organization | None:
        """Return an organization by business code."""
        raise NotImplementedError

    @abstractmethod
    def code_exists(self, code: OrganizationCode) -> bool:
        """Return whether an organization code is already registered."""
        raise NotImplementedError
