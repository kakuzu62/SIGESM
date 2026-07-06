from __future__ import annotations

import logging
from collections.abc import Callable, Mapping
from types import TracebackType
from typing import Any, TypeVar

from sqlalchemy import Executable, Result
from sqlalchemy.orm import Session

from core.database.session import DatabaseSessionFactory
from domain.contracts.unit_of_work import IUnitOfWork
from infrastructure.persistence.sqlalchemy.session_context import SessionContext
from infrastructure.persistence.sqlalchemy.transaction_manager import TransactionManager

RepositoryT = TypeVar("RepositoryT")
logger = logging.getLogger(__name__)


class SqlAlchemyUnitOfWork(IUnitOfWork):
    """SQLAlchemy implementation of the unit of work contract."""

    def __init__(self, session_factory: DatabaseSessionFactory) -> None:
        self._session_factory = session_factory
        self._session_context: SessionContext | None = None
        self._transaction_manager: TransactionManager | None = None
        self.session: Session | None = None
        self.repositories: dict[str, object] = {}

    def __enter__(self) -> SqlAlchemyUnitOfWork:
        self.begin()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        if exc_type is None:
            self.commit()
        else:
            if exc is not None:
                logger.exception("Erro SQL na unidade de trabalho.", exc_info=exc)
            self.rollback()
        self.close()

    def begin(self) -> None:
        """Open a session and start a transaction."""
        self._session_context = SessionContext(self._session_factory)
        self.session = self._session_context.__enter__()
        self._transaction_manager = TransactionManager(self.session)
        self._transaction_manager.begin()

    def commit(self) -> None:
        """Commit the current transaction."""
        self._require_transaction().commit()
        logger.info("Commit executado pela unidade de trabalho SQLAlchemy.")

    def rollback(self) -> None:
        """Rollback the current transaction."""
        self._require_transaction().rollback()
        logger.info("Rollback executado pela unidade de trabalho SQLAlchemy.")

    def close(self) -> None:
        """Dispose the current session and registered repositories."""
        if self._session_context is not None:
            self._session_context.__exit__(None, None, None)
        self.repositories.clear()
        self._transaction_manager = None
        self._session_context = None
        self.session = None
        logger.info("Unidade de trabalho SQLAlchemy descartada.")

    def flush(self) -> None:
        """Flush pending changes to the database."""
        self._require_session().flush()

    def execute(
        self,
        statement: object,
        parameters: Mapping[str, object] | None = None,
    ) -> Result[Any]:
        """Execute a SQLAlchemy statement inside the active session."""
        if not isinstance(statement, Executable):
            raise TypeError("SqlAlchemyUnitOfWork requires a SQLAlchemy executable statement.")

        return self._require_session().execute(statement, parameters)

    def repository(self, key: str, factory: Callable[[Session], RepositoryT]) -> RepositoryT:
        """Resolve and cache a repository for this unit of work."""
        if key not in self.repositories:
            self.repositories[key] = factory(self._require_session())

        return self.repositories[key]  # type: ignore[return-value]

    def _require_session(self) -> Session:
        """Return the active session or raise when closed."""
        if self.session is None:
            raise RuntimeError("SqlAlchemyUnitOfWork nao foi iniciada.")
        return self.session

    def _require_transaction(self) -> TransactionManager:
        """Return the active transaction manager or raise when closed."""
        if self._transaction_manager is None:
            raise RuntimeError("Transacao da SqlAlchemyUnitOfWork nao foi iniciada.")
        return self._transaction_manager
