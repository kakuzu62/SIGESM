"""Domain contracts exposed to application use cases."""

from domain.contracts.repository import IRepository
from domain.contracts.unit_of_work import IUnitOfWork

__all__ = ["IRepository", "IUnitOfWork"]
