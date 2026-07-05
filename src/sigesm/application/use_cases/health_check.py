from __future__ import annotations

from dataclasses import dataclass

from sigesm.application.ports import UnitOfWorkFactory


@dataclass(frozen=True, kw_only=True)
class HealthCheckResult:
    database_available: bool


class RunHealthCheck:
    def __init__(self, unit_of_work_factory: UnitOfWorkFactory) -> None:
        self._unit_of_work_factory = unit_of_work_factory

    def execute(self) -> HealthCheckResult:
        with self._unit_of_work_factory.create() as unit_of_work:
            unit_of_work.commit()
        return HealthCheckResult(database_available=True)
