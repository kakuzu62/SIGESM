from __future__ import annotations

import os

from dotenv import load_dotenv

load_dotenv()


class Environment:
    @staticmethod
    def get(key: str, default: str | None = None) -> str | None:
        return os.getenv(key, default)

    @staticmethod
    def get_bool(key: str, default: bool = False) -> bool:
        value = os.getenv(key)

        if value is None:
            return default

        return value.lower() in (
            "1",
            "true",
            "yes",
            "on",
        )
