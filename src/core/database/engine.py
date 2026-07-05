from __future__ import annotations

import logging
from pathlib import Path

from sqlalchemy import Engine, create_engine
from sqlalchemy.engine import make_url

from core.config.settings import DatabaseSettings, settings

logger = logging.getLogger(__name__)


class DatabaseEngineFactory:
    """Factory responsible for creating configured SQLAlchemy engines."""

    def __init__(self, database_settings: DatabaseSettings | None = None) -> None:
        self._settings = database_settings or settings.database

    def create(self) -> Engine:
        """Create a SQLAlchemy engine compatible with SQLite and PostgreSQL."""
        database_url = self._settings.url
        url = make_url(database_url)
        connect_args: dict[str, object] = {}
        engine_options: dict[str, object] = {
            "echo": self._settings.echo,
            "future": True,
            "pool_pre_ping": self._settings.pool_pre_ping,
        }

        if url.get_backend_name() == "sqlite":
            self._ensure_sqlite_parent_directory(url.database)
            connect_args["check_same_thread"] = False
        else:
            engine_options["pool_size"] = self._settings.pool_size
            engine_options["max_overflow"] = self._settings.max_overflow

        logger.info("Criando engine de banco de dados para provider %s.", self._settings.provider)
        return create_engine(database_url, connect_args=connect_args, **engine_options)

    def _ensure_sqlite_parent_directory(self, database_path: str | None) -> None:
        """Create the SQLite parent directory when the database is file-based."""
        if database_path is None or database_path in ("", ":memory:"):
            return

        Path(database_path).parent.mkdir(parents=True, exist_ok=True)
