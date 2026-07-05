from __future__ import annotations

from dataclasses import dataclass

from sigesm.application.ports import UnitOfWorkFactory
from sigesm.application.use_cases import RunHealthCheck
from sigesm.config.settings import Settings
from sigesm.infrastructure.database.session import DatabaseSessionFactory


@dataclass(frozen=True, kw_only=True)
class ApplicationContainer:
    settings: Settings
    session_factory: DatabaseSessionFactory
    unit_of_work_factory: UnitOfWorkFactory

    def health_check(self) -> RunHealthCheck:
        return RunHealthCheck(unit_of_work_factory=self.unit_of_work_factory)
