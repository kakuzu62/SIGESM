from __future__ import annotations

from sqlalchemy import Column, Integer, String, select

from core.config.settings import DatabaseSettings
from core.database.base import Base
from core.database.engine import DatabaseEngineFactory
from core.database.healthcheck import DatabaseHealthCheck
from core.database.session import DatabaseSessionFactory
from infrastructure.persistence.repository import SqlAlchemyRepository
from infrastructure.persistence.unit_of_work import UnitOfWork


class PersistenceSmokeModel(Base):
    """Persistence model used to validate infrastructure wiring."""

    __tablename__ = "persistence_smoke"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)


class PersistenceSmokeRepository(SqlAlchemyRepository[PersistenceSmokeModel, int]):
    """Repository used by persistence infrastructure tests."""

    entity_type = PersistenceSmokeModel


def test_database_healthcheck_validates_engine_session_and_connection(tmp_path) -> None:
    database_settings = DatabaseSettings(database=str(tmp_path / "healthcheck.db"))
    session_factory = DatabaseSessionFactory.from_engine_factory(
        DatabaseEngineFactory(database_settings)
    )

    status = DatabaseHealthCheck(session_factory).execute()

    assert status.healthy is True


def test_unit_of_work_commits_repository_changes(tmp_path) -> None:
    database_settings = DatabaseSettings(database=str(tmp_path / "repository.db"))
    session_factory = DatabaseSessionFactory.from_engine_factory(
        DatabaseEngineFactory(database_settings)
    )
    Base.metadata.create_all(session_factory.engine)

    with UnitOfWork(session_factory) as unit_of_work:
        repository = PersistenceSmokeRepository(unit_of_work.session)
        repository.add(PersistenceSmokeModel(id=1, name="SIGESM"))

    with session_factory.context() as session:
        result = session.execute(select(PersistenceSmokeModel.name)).scalar_one()

    assert result == "SIGESM"
