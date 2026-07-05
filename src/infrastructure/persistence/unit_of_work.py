from __future__ import annotations

import logging
from types import TracebackType

from sqlalchemy.orm import Session

from core.database.session import DatabaseSessionFactory

logger = logging.getLogger(__name__)


class UnitOfWork:
    """Coordinates session and transaction boundaries for application use cases."""

    def __init__(self, session_factory: DatabaseSessionFactory) -> None:
        self._session_factory = session_factory
        self.session: Session | None = None

    def __enter__(self) -> UnitOfWork:
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
                logger.exception("Erro durante unidade de trabalho.", exc_info=exc)
            else:
                logger.error("Erro durante unidade de trabalho.")
            self.rollback()

        self.close()

    def begin(self) -> None:
        """Open a session and begin a transaction."""
        logger.info("Abrindo unidade de trabalho.")
        self.session = self._session_factory.create()
        self.session.begin()

    def commit(self) -> None:
        """Commit the current unit of work."""
        self._require_session().commit()
        logger.info("Commit da unidade de trabalho concluido.")

    def rollback(self) -> None:
        """Rollback the current unit of work."""
        self._require_session().rollback()
        logger.info("Rollback da unidade de trabalho concluido.")

    def close(self) -> None:
        """Close the current unit of work session."""
        session = self._require_session()
        session.close()
        self._session_factory.remove()
        self.session = None
        logger.info("Unidade de trabalho fechada.")

    def _require_session(self) -> Session:
        """Return the active session or raise when the unit of work is not open."""
        if self.session is None:
            raise RuntimeError("UnitOfWork nao foi iniciada.")

        return self.session
