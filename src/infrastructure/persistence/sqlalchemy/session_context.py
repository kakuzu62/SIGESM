from __future__ import annotations

import logging
from types import TracebackType

from sqlalchemy.orm import Session

from core.database.session import DatabaseSessionFactory

logger = logging.getLogger(__name__)


class SessionContext:
    """Context manager responsible for opening and closing SQLAlchemy sessions."""

    def __init__(self, session_factory: DatabaseSessionFactory) -> None:
        self._session_factory = session_factory
        self._session: Session | None = None

    def __enter__(self) -> Session:
        self._session = self._session_factory.create()
        logger.info("Sessao SQLAlchemy aberta.")
        return self._session

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        if exc is not None:
            logger.exception("Erro SQL durante contexto de sessao.", exc_info=exc)

        if self._session is not None:
            self._session.close()
            self._session_factory.remove()
            logger.info("Sessao SQLAlchemy encerrada.")
            self._session = None
