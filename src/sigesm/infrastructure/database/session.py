from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

from sqlalchemy import Engine, create_engine, event
from sqlalchemy.engine import make_url
from sqlalchemy.orm import Session, sessionmaker

from sigesm.config.settings import Settings


class DatabaseSessionFactory:
    def __init__(self, engine: Engine, session_maker: sessionmaker[Session]) -> None:
        self.engine = engine
        self._session_maker = session_maker

    @classmethod
    def from_settings(cls, settings: Settings) -> DatabaseSessionFactory:
        url = make_url(settings.database.url)
        if url.get_backend_name() == "sqlite" and url.database not in (None, "", ":memory:"):
            Path(url.database).parent.mkdir(parents=True, exist_ok=True)

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
    def set_sqlite_pragma(dbapi_connection: object, _connection_record: object) -> None:
        cursor = dbapi_connection.cursor()
        try:
            cursor.execute("PRAGMA foreign_keys=ON")
        finally:
            cursor.close()
