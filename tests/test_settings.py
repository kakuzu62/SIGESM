from __future__ import annotations

from sigesm.config.settings import Settings


def test_settings_uses_sqlite_database_by_default() -> None:
    settings = Settings()

    assert settings.database.is_sqlite
    assert settings.database.url == "sqlite:///database/sigesm.db"
