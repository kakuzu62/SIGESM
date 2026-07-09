from __future__ import annotations

from pathlib import Path


class QssLoader:
    """Loads Qt stylesheet files with a safe fallback."""

    def load(self, path: Path) -> str:
        """Return QSS content or an empty stylesheet when the file is missing."""
        if not path.exists() or not path.is_file():
            return ""
        return path.read_text(encoding="utf-8")
