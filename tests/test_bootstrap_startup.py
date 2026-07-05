from __future__ import annotations

from bootstrap.startup import Startup


def test_startup_prints_environment_and_database(capsys, tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)

    Startup().initialize()

    output = capsys.readouterr().out
    assert "SIGESM Enterprise" in output
    assert "Environment : Development" in output
    assert "Database    : sqlite" in output
    assert (tmp_path / "logs" / "sigesm.log").exists()
