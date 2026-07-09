from __future__ import annotations

from pathlib import Path


class ResourceCatalog:
    """Resolves presentation resources from a base directory."""

    def __init__(self, base_path: Path) -> None:
        self._base_path = base_path

    def resolve(self, relative_path: str) -> Path:
        """Resolve a resource path without loading it."""
        return self._base_path / relative_path
