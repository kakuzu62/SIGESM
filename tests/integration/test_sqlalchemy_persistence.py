from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path

import pytest
from sqlalchemy import select
from sqlalchemy.orm import Mapped, mapped_column

from application.common.filters import FilterExpression, FilterGroup, FilterOperator
from application.common.ordering import Ordering, SortDirection
from application.common.pagination import Pagination
from core.config.settings import DatabaseSettings
from core.database.base import Base
from core.database.engine import DatabaseEngineFactory
from core.database.session import DatabaseSessionFactory
from infrastructure.persistence.sqlalchemy.base_repository import SqlAlchemyBaseRepository
from infrastructure.persistence.sqlalchemy.session_context import SessionContext
from infrastructure.persistence.sqlalchemy.transaction_manager import TransactionManager
from infrastructure.persistence.sqlalchemy.unit_of_work import SqlAlchemyUnitOfWork


class InventoryItemModel(Base):
    """Persistence model used to validate SQLAlchemy infrastructure."""

    __tablename__ = "inventory_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False)


class InventoryItemRepository(SqlAlchemyBaseRepository[InventoryItemModel, int]):
    """Repository used by SQLAlchemy persistence tests."""

    model_type = InventoryItemModel


@pytest.fixture
def session_factory(tmp_path: Path) -> Iterator[DatabaseSessionFactory]:
    """Create an isolated SQLite session factory for persistence tests."""
    database_settings = DatabaseSettings(database=str(tmp_path / "persistence.db"))
    factory = DatabaseSessionFactory.from_engine_factory(DatabaseEngineFactory(database_settings))
    Base.metadata.create_all(factory.engine)
    yield factory
    Base.metadata.drop_all(factory.engine)


def test_session_context_opens_and_closes_session(session_factory: DatabaseSessionFactory) -> None:
    with SessionContext(session_factory) as session:
        assert session.is_active
        session.execute(select(1))


def test_repository_supports_common_operations(session_factory: DatabaseSessionFactory) -> None:
    with SessionContext(session_factory) as session:
        repository = InventoryItemRepository(session)
        repository.insert(InventoryItemModel(id=1, name="Monitor", quantity=5))
        repository.insert(InventoryItemModel(id=2, name="Mouse", quantity=10))
        session.commit()

        filtered = repository.filter(
            FilterGroup(
                expressions=(
                    FilterExpression(
                        field="quantity",
                        operator=FilterOperator.GREATER_THAN,
                        value=6,
                    ),
                )
            )
        )
        ordered = repository.order_by(Ordering(field="name", direction=SortDirection.DESC))
        page = repository.paginate(Pagination(page=1, page_size=1), ordering=Ordering(field="id"))

        assert repository.exists(1)
        monitor = repository.get(1)
        mouse = repository.get_by_id(2)
        assert monitor is not None
        assert mouse is not None
        assert monitor.name == "Monitor"
        assert mouse.name == "Mouse"
        assert repository.count() == 2
        assert repository.first() is not None
        assert len(repository.list()) == 2
        assert tuple(item.name for item in filtered) == ("Mouse",)
        assert tuple(item.name for item in ordered) == ("Mouse", "Monitor")
        assert page.total_items == 2
        assert page.items[0].name == "Monitor"

        item = repository.get_by_id(1)
        assert item is not None
        item.quantity = 7
        repository.update(item)
        repository.delete_by_id(2)
        session.commit()

        assert repository.count() == 1


def test_transaction_manager_supports_nested_savepoint(
    session_factory: DatabaseSessionFactory,
) -> None:
    with SessionContext(session_factory) as session:
        manager = TransactionManager(session)
        manager.begin()
        session.add(InventoryItemModel(id=1, name="Keyboard", quantity=3))
        nested = manager.savepoint()
        session.add(InventoryItemModel(id=2, name="Cable", quantity=8))
        nested.rollback()
        manager.commit()

    with SessionContext(session_factory) as session:
        names = tuple(session.scalars(select(InventoryItemModel.name)).all())

    assert names == ("Keyboard",)


def test_sqlalchemy_unit_of_work_commits_and_caches_repositories(
    session_factory: DatabaseSessionFactory,
) -> None:
    with SqlAlchemyUnitOfWork(session_factory) as unit_of_work:
        repository = unit_of_work.repository("items", InventoryItemRepository)
        same_repository = unit_of_work.repository("items", InventoryItemRepository)
        repository.insert(InventoryItemModel(id=1, name="Notebook", quantity=2))
        unit_of_work.flush()

        assert repository is same_repository

    with SessionContext(session_factory) as session:
        assert session.execute(select(InventoryItemModel.name)).scalar_one() == "Notebook"


def test_sqlalchemy_unit_of_work_rolls_back_on_error(
    session_factory: DatabaseSessionFactory,
) -> None:
    with pytest.raises(RuntimeError):
        with SqlAlchemyUnitOfWork(session_factory) as unit_of_work:
            repository = unit_of_work.repository("items", InventoryItemRepository)
            repository.insert(InventoryItemModel(id=1, name="Dock", quantity=1))
            raise RuntimeError("forced rollback")

    with SessionContext(session_factory) as session:
        assert session.execute(select(InventoryItemModel)).scalar_one_or_none() is None
