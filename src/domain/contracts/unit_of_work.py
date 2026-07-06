from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Mapping


class IUnitOfWork(ABC):
    """Domain contract for transaction boundary management."""

    @abstractmethod
    def begin(self) -> None:
        """Begin a transactional unit of work."""
        raise NotImplementedError

    @abstractmethod
    def commit(self) -> None:
        """Commit pending changes."""
        raise NotImplementedError

    @abstractmethod
    def rollback(self) -> None:
        """Rollback pending changes."""
        raise NotImplementedError

    @abstractmethod
    def close(self) -> None:
        """Dispose resources owned by this unit of work."""
        raise NotImplementedError

    @abstractmethod
    def flush(self) -> None:
        """Flush pending changes to the database transaction."""
        raise NotImplementedError

    @abstractmethod
    def execute(
        self,
        statement: object,
        parameters: Mapping[str, object] | None = None,
    ) -> object:
        """Execute an implementation-specific statement inside this unit of work."""
        raise NotImplementedError
