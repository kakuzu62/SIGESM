from __future__ import annotations

from bootstrap.startup import Startup


class Application:
    def __init__(self) -> None:
        self._startup = Startup()

    def run(self) -> None:
        self._startup.initialize()
