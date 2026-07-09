from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class WorkspaceDocument:
    """Descriptor for an opened workspace document or view."""

    key: str
    title: str
    route: str


class WorkspaceManager:
    """Tracks opened workspace documents."""

    def __init__(self) -> None:
        self._documents: dict[str, WorkspaceDocument] = {}

    def open(self, document: WorkspaceDocument) -> None:
        """Open or replace a workspace document."""
        self._documents[document.key] = document

    def close(self, key: str) -> None:
        """Close a workspace document."""
        self._documents.pop(key, None)

    @property
    def documents(self) -> tuple[WorkspaceDocument, ...]:
        """Return opened workspace documents."""
        return tuple(self._documents.values())
