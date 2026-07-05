from __future__ import annotations

import logging
from types import TracebackType

from sqlalchemy.orm import Session, SessionTransaction

logger = logging.getLogger(__name__)


class Transaction:
    """Manages a SQLAlchemy transaction lifecycle."""

    def __init__(self, session: Session) -> None:
        self._session = session
        self._transaction: SessionTransaction | None = None

    def __enter__(self) -> Transaction:
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
            logger.exception("Erro durante transacao de banco de dados.", exc_info=exc)
        else:
            logger.error("Erro durante transacao de banco de dados.")
        self.rollback()

    def begin(self) -> None:
        """Begin a database transaction."""
        logger.info("Abrindo transacao de banco de dados.")
        self._transaction = self._session.begin()

    def commit(self) -> None:
        """Commit the active database transaction."""
        logger.info("Confirmando transacao de banco de dados.")
        if self._transaction is not None:
            self._transaction.commit()
            self._transaction = None

    def rollback(self) -> None:
        """Rollback the active database transaction."""
        logger.info("Revertendo transacao de banco de dados.")
        if self._transaction is not None:
            self._transaction.rollback()
            self._transaction = None
