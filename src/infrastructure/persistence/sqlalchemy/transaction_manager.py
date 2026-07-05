from __future__ import annotations

import logging
from time import perf_counter
from types import TracebackType

from sqlalchemy.orm import Session, SessionTransaction

logger = logging.getLogger(__name__)


class TransactionManager:
    """Manages root and nested SQLAlchemy transactions with timing logs."""

    def __init__(self, session: Session) -> None:
        self._session = session
        self._transaction: SessionTransaction | None = None
        self._started_at: float | None = None

    def __enter__(self) -> TransactionManager:
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
            return

        if exc is not None:
            logger.exception("Erro SQL durante transacao.", exc_info=exc)
        self.rollback()

    def begin(self) -> None:
        """Begin a root transaction."""
        self._started_at = perf_counter()
        self._transaction = self._session.begin()
        logger.info("Transacao SQLAlchemy iniciada.")

    def begin_nested(self) -> SessionTransaction:
        """Begin a nested transaction savepoint."""
        logger.info("Savepoint SQLAlchemy iniciado.")
        return self._session.begin_nested()

    def savepoint(self) -> SessionTransaction:
        """Create a savepoint using a nested transaction."""
        return self.begin_nested()

    def commit(self) -> None:
        """Commit the active transaction."""
        if self._transaction is not None:
            self._transaction.commit()
            self._transaction = None
        logger.info("Commit SQLAlchemy concluido em %.6fs.", self._elapsed())

    def rollback(self) -> None:
        """Rollback the active transaction."""
        if self._transaction is not None:
            self._transaction.rollback()
            self._transaction = None
        logger.info("Rollback SQLAlchemy concluido em %.6fs.", self._elapsed())

    def _elapsed(self) -> float:
        """Return transaction elapsed time in seconds."""
        if self._started_at is None:
            return 0.0

        elapsed = perf_counter() - self._started_at
        self._started_at = None
        return elapsed
