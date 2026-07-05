from __future__ import annotations

from abc import abstractmethod

from domain.contracts.repository import IRepository
from domain.military.entities import MilitaryPerson
from domain.military.value_objects import CPF, MilitaryId
from shared.kernel.identity import Identity


class IMilitaryRepository(IRepository[MilitaryPerson, Identity]):
    """Repository contract for military person aggregates."""

    @abstractmethod
    def get_by_military_id(self, military_id: MilitaryId) -> MilitaryPerson | None:
        """Return a military person by military identifier."""
        raise NotImplementedError

    @abstractmethod
    def get_by_cpf(self, cpf: CPF) -> MilitaryPerson | None:
        """Return a military person by CPF."""
        raise NotImplementedError
