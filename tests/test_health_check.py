from __future__ import annotations

from pathlib import Path

from sigesm.bootstrap import build_application
from sigesm.config.settings import DatabaseSettings, Settings


def test_health_check_opens_database_transaction(tmp_path: Path) -> None:
    database_settings = DatabaseSettings().model_copy(
        update={"url": f"sqlite:///{tmp_path / 'sigesm.db'}"}
    )
    settings = Settings(database=database_settings)
    container = build_application(settings)

    result = container.health_check().execute()

    assert result.database_available is True
