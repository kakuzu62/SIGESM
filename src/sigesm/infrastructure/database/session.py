from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from typing import Protocol

from sqlalchemy import Engine, create_engine, event
from sqlalchemy.engine import make_url
from sqlalchemy.orm import Session, sessionmaker

from sigesm.config.settings import Settings


class _DatabaseCursor(Protocol):
    """Minimal DB-API cursor contract used for SQLite initialization."""

    def execute(self, statement: str) -> object:
        """Execute a database statement."""
        raise NotImplementedError

    def close(self) -> None:
        """Close the cursor."""
        raise NotImplementedError


class _DatabaseConnection(Protocol):
    """Minimal DB-API connection contract used by SQLAlchemy events."""

    def cursor(self) -> _DatabaseCursor:
        """Return a DB-API cursor."""
        raise NotImplementedError


class DatabaseSessionFactory:
    def __init__(self, engine: Engine, session_maker: sessionmaker[Session]) -> None:
        self.engine = engine
        self._session_maker = session_maker

    @classmethod
    def from_settings(cls, settings: Settings) -> DatabaseSessionFactory:
        url = make_url(settings.database.url)
        database_path = url.database
        if (
            url.get_backend_name() == "sqlite"
            and isinstance(database_path, str)
            and database_path not in ("", ":memory:")
        ):
            Path(database_path).parent.mkdir(parents=True, exist_ok=True)

        connect_args: dict[str, object] = {}
        if url.get_backend_name() == "sqlite":
            connect_args["check_same_thread"] = False

        engine = create_engine(
            url,
            echo=settings.database.echo,
            future=True,
            pool_pre_ping=settings.database.pool_pre_ping,
            connect_args=connect_args,
        )
        if url.get_backend_name() == "sqlite":
            _enable_sqlite_foreign_keys(engine)

        return cls(
            engine=engine,
            session_maker=sessionmaker(
                bind=engine,
                autoflush=False,
                expire_on_commit=False,
                future=True,
            ),
        )

    @contextmanager
    def create(self) -> Iterator[Session]:
        session = self._session_maker()
        try:
            yield session
        finally:
            session.close()


def _enable_sqlite_foreign_keys(engine: Engine) -> None:
    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(
        dbapi_connection: _DatabaseConnection,
        _connection_record: object,
    ) -> None:
        cursor = dbapi_connection.cursor()
        try:
            cursor.execute("PRAGMA foreign_keys=ON")
        finally:
            cursor.close()
