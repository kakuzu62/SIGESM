from __future__ import annotations

from domain.organization.repositories import IOrganizationRepository
from domain.organization.value_objects import OrganizationCode
from shared.kernel.specification import Specification


class OrganizationCodeAlreadyExists(Specification[OrganizationCode]):
    """Specification that checks whether an organization code is already in use."""

    def __init__(self, repository: IOrganizationRepository) -> None:
        self._repository = repository

    def is_satisfied_by(self, candidate: OrganizationCode) -> bool:
        """Return whether the candidate code already exists."""
        return self._repository.code_exists(candidate)
