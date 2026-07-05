from __future__ import annotations

import logging
from collections.abc import Iterator
from contextlib import contextmanager

from sqlalchemy import Engine
from sqlalchemy.orm import Session, scoped_session, sessionmaker

from core.database.engine import DatabaseEngineFactory

logger = logging.getLogger(__name__)


class DatabaseSessionFactory:
    """Thread-safe SQLAlchemy session factory with context manager support."""

    def __init__(self, engine: Engine) -> None:
        self._engine = engine
        self._sessionmaker = sessionmaker(
            bind=self._engine,
            autoflush=False,
            expire_on_commit=False,
            future=True,
        )
        self._scoped_session = scoped_session(self._sessionmaker)

    @classmethod
    def from_engine_factory(
        cls,
        engine_factory: DatabaseEngineFactory | None = None,
    ) -> DatabaseSessionFactory:
        """Create a session factory from the configured engine factory."""
        factory = engine_factory or DatabaseEngineFactory()
        return cls(engine=factory.create())

    @property
    def engine(self) -> Engine:
        """Return the engine associated with this session factory."""
        return self._engine

    def create(self) -> Session:
        """Open a scoped session for the current execution context."""
        logger.info("Abrindo sessao de banco de dados.")
        return self._scoped_session()

    def remove(self) -> None:
        """Remove the current scoped session."""
        logger.info("Fechando sessao scoped de banco de dados.")
        self._scoped_session.remove()

    @contextmanager
    def context(self) -> Iterator[Session]:
        """Yield a session and guarantee closure when leaving the context."""
        session = self.create()
        try:
            yield session
        except Exception:
            logger.exception("Erro durante uso da sessao de banco de dados.")
            raise
        finally:
            logger.info("Fechando sessao de banco de dados.")
            session.close()
            self.remove()
