from __future__ import annotations

from types import TracebackType
from typing import Protocol


class UnitOfWork(Protocol):
    def __enter__(self) -> UnitOfWork:
        raise NotImplementedError

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        raise NotImplementedError

    def commit(self) -> None:
        raise NotImplementedError

    def rollback(self) -> None:
        raise NotImplementedError


class UnitOfWorkFactory(Protocol):
    def create(self) -> UnitOfWork:
        raise NotImplementedError
