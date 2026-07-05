from __future__ import annotations

from core.config.loader import Loader
from core.config.paths import CONFIG, DATABASE, LOGS, RESOURCES
from core.constants.application import APPLICATION_NAME, DEFAULT_LANGUAGE, DEFAULT_THEME
from core.resources.manager import ResourceManager


def test_loader_creates_required_runtime_directories() -> None:
    Loader.initialize()

    assert CONFIG.exists()
    assert DATABASE.exists()
    assert LOGS.exists()


def test_resource_manager_resolves_resource_paths() -> None:
    assert ResourceManager.resource("icons") == RESOURCES / "icons"


def test_application_constants_are_available() -> None:
    assert APPLICATION_NAME == "SIGESM Enterprise"
    assert DEFAULT_THEME == "dark"
    assert DEFAULT_LANGUAGE == "pt_BR"
