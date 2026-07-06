from __future__ import annotations

from pathlib import Path

from bootstrap.startup import Startup
from pytest import CaptureFixture, MonkeyPatch


def test_startup_prints_environment_and_database(
    capsys: CaptureFixture[str],
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    monkeypatch.chdir(tmp_path)

    Startup().initialize()

    output = capsys.readouterr().out
    assert "SIGESM Enterprise" in output
    assert "Environment : Development" in output
    assert "Database    : sqlite" in output
    assert (tmp_path / "logs" / "sigesm.log").exists()
