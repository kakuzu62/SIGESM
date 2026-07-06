from __future__ import annotations

from pathlib import Path

from bootstrap.startup import Startup
from pytest import CaptureFixture, MonkeyPatch


def test_startup_initializes_environment_and_logging(
    capsys: CaptureFixture[str],
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    monkeypatch.chdir(tmp_path)

    Startup().initialize()

    output = capsys.readouterr().out
    assert output == ""
    assert (tmp_path / "logs" / "sigesm.log").exists()
    assert "SIGESM Enterprise initialized" in (tmp_path / "logs" / "sigesm.log").read_text(
        encoding="utf-8"
    )
