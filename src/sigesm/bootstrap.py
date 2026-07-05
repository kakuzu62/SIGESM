from __future__ import annotations

from sigesm.config.settings import Settings, get_settings
from sigesm.infrastructure.database.session import DatabaseSessionFactory
from sigesm.infrastructure.database.uow import SqlAlchemyUnitOfWorkFactory
from sigesm.infrastructure.di.container import ApplicationContainer


def build_application(settings: Settings | None = None) -> ApplicationContainer:
    resolved_settings = settings or get_settings()
    session_factory = DatabaseSessionFactory.from_settings(resolved_settings)
    unit_of_work_factory = SqlAlchemyUnitOfWorkFactory(session_factory=session_factory)
    return ApplicationContainer(
        settings=resolved_settings,
        session_factory=session_factory,
        unit_of_work_factory=unit_of_work_factory,
    )
