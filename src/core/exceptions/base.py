from __future__ import annotations


class SIGESMException(Exception):
    """Base exception for all SIGESM Enterprise failures."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
