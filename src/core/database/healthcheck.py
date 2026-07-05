from __future__ import annotations

import logging
from dataclasses import dataclass

from sqlalchemy import text

from core.database.session import DatabaseSessionFactory

logger = logging.getLogger(__name__)


@dataclass(slots=True, frozen=True)
class DatabaseHealthStatus:
    """Result of a database infrastructure health check."""

    engine_available: bool
    session_available: bool
    connection_available: bool

    @property
    def healthy(self) -> bool:
        """Return whether all persistence infrastructure checks passed."""
        return self.engine_available and self.session_available and self.connection_available


class DatabaseHealthCheck:
    """Validates engine, session and connection availability."""

    def __init__(self, session_factory: DatabaseSessionFactory) -> None:
        self._session_factory = session_factory

    def execute(self) -> DatabaseHealthStatus:
        """Run a database health check using a lightweight SQL statement."""
        try:
            engine_available = self._session_factory.engine is not None
            with self._session_factory.context() as session:
                session.execute(text("SELECT 1"))
                session_available = session.is_active

            return DatabaseHealthStatus(
                engine_available=engine_available,
                session_available=session_available,
                connection_available=True,
            )
        except Exception:
            logger.exception("Falha no healthcheck de banco de dados.")
            return DatabaseHealthStatus(
                engine_available=False,
                session_available=False,
                connection_available=False,
            )
