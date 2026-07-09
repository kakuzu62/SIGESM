from __future__ import annotations

from pathlib import Path


class DesktopResourceManager:
    """Centralizes desktop resource path resolution."""

    def __init__(self, root: Path) -> None:
        self._root = root

    def resolve(self, relative_path: str) -> Path:
        """Resolve a resource path."""
        return self._root / relative_path

    def style(self, name: str) -> Path:
        """Resolve a style resource."""
        return self.resolve(f"styles/{name}")

    def icon(self, name: str) -> Path:
        """Resolve an icon resource."""
        return self.resolve(f"icons/{name}")

    def image(self, name: str) -> Path:
        """Resolve an image resource."""
        return self.resolve(f"images/{name}")
