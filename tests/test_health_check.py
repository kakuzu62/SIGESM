from __future__ import annotations

from sigesm.bootstrap import build_application
from sigesm.config.settings import DatabaseSettings, Settings


def test_health_check_opens_database_transaction(tmp_path) -> None:
    settings = Settings(database=DatabaseSettings(url=f"sqlite:///{tmp_path / 'sigesm.db'}"))
    container = build_application(settings)

    result = container.health_check().execute()

    assert result.database_available is True
