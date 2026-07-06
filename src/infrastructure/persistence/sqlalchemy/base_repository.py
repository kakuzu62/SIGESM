from __future__ import annotations

from collections.abc import Sequence
from typing import Any, Generic, TypeVar, cast

from sqlalchemy import Select, delete, func, inspect, select
from sqlalchemy.engine import CursorResult
from sqlalchemy.orm import InstrumentedAttribute, Mapper, Session

from application.common.filters import FilterExpression, FilterGroup, FilterOperator
from application.common.ordering import Ordering, SortDirection
from application.common.pagination import PageResult, Pagination
from domain.contracts.repository import IRepository

ModelT = TypeVar("ModelT")
EntityIdT = TypeVar("EntityIdT")


class SqlAlchemyBaseRepository(IRepository[ModelT, EntityIdT], Generic[ModelT, EntityIdT]):
    """Production SQLAlchemy repository base with common query operations."""

    model_type: type[ModelT]

    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, entity: ModelT) -> ModelT:
        """Add an entity to the current SQLAlchemy session."""
        return self.insert(entity)

    def insert(self, entity: ModelT) -> ModelT:
        """Insert an entity in the current SQLAlchemy session."""
        self._session.add(entity)
        return entity

    def update(self, entity: ModelT) -> ModelT:
        """Merge an entity into the current SQLAlchemy session."""
        return self._session.merge(entity)

    def delete(self, entity: ModelT) -> None:
        """Delete an entity from the current SQLAlchemy session."""
        self._session.delete(entity)

    def delete_by_id(self, entity_id: EntityIdT) -> int:
        """Delete an entity by identifier and return affected rows."""
        primary_key = self._primary_key_attribute()
        result = cast(
            CursorResult[Any],
            self._session.execute(delete(self.model_type).where(primary_key == entity_id)),
        )
        return result.rowcount or 0

    def exists(self, entity_id: EntityIdT) -> bool:
        """Return whether an entity exists for the given identifier."""
        primary_key = self._primary_key_attribute()
        statement = (
            select(func.count()).select_from(self.model_type).where(primary_key == entity_id)
        )
        return self._session.execute(statement).scalar_one() > 0

    def get_by_id(self, entity_id: EntityIdT) -> ModelT | None:
        """Return an entity by identifier."""
        return self.get(entity_id)

    def get(self, entity_id: EntityIdT) -> ModelT | None:
        """Return an entity by identifier."""
        return self._session.get(self.model_type, entity_id)

    def list(self) -> Sequence[ModelT]:
        """Return all entities ordered by natural database order."""
        return tuple(self._session.scalars(select(self.model_type)).all())

    def count(self) -> int:
        """Return the total number of entities."""
        statement = select(func.count()).select_from(self.model_type)
        return self._session.execute(statement).scalar_one()

    def first(self) -> ModelT | None:
        """Return the first entity from the repository."""
        return self._session.scalars(select(self.model_type).limit(1)).first()

    def paginate(
        self,
        pagination: Pagination,
        filters: FilterGroup | None = None,
        ordering: Ordering | None = None,
    ) -> PageResult[ModelT]:
        """Return a paginated result applying optional filters and ordering."""
        statement = self._apply_filters(select(self.model_type), filters)
        statement = self._apply_ordering(statement, ordering)
        total = self.count_filtered(filters)
        items = tuple(
            self._session.scalars(
                statement.offset(pagination.offset).limit(pagination.page_size)
            ).all()
        )
        return PageResult(
            items=items,
            total_items=total,
            page=pagination.page,
            page_size=pagination.page_size,
        )

    def filter(self, filters: FilterGroup) -> Sequence[ModelT]:
        """Return entities matching a filter group."""
        statement = self._apply_filters(select(self.model_type), filters)
        return tuple(self._session.scalars(statement).all())

    def order_by(self, ordering: Ordering) -> Sequence[ModelT]:
        """Return entities ordered by a field expression."""
        statement = self._apply_ordering(select(self.model_type), ordering)
        return tuple(self._session.scalars(statement).all())

    def count_filtered(self, filters: FilterGroup | None) -> int:
        """Return entity count matching a filter group."""
        statement = self._apply_filters(select(func.count()).select_from(self.model_type), filters)
        return int(self._session.execute(statement).scalar_one())

    def _apply_filters(
        self, statement: Select[tuple[Any, ...]], filters: FilterGroup | None
    ) -> Select[tuple[Any, ...]]:
        """Apply filter expressions to a SQLAlchemy select statement."""
        if filters is None:
            return statement

        filtered_statement = statement
        for expression in filters.expressions:
            filtered_statement = filtered_statement.where(self._build_filter_clause(expression))
        return filtered_statement

    def _apply_ordering(
        self,
        statement: Select[tuple[Any, ...]],
        ordering: Ordering | None,
    ) -> Select[tuple[Any, ...]]:
        """Apply ordering to a SQLAlchemy select statement."""
        if ordering is None:
            return statement

        column = self._column(ordering.field)
        ordered_column = column.desc() if ordering.direction == SortDirection.DESC else column.asc()
        return statement.order_by(ordered_column)

    def _build_filter_clause(self, expression: FilterExpression) -> Any:
        """Build a SQLAlchemy clause for a filter expression."""
        column = self._column(expression.field)
        value = expression.value

        if expression.operator == FilterOperator.EQUALS:
            return column == value
        if expression.operator == FilterOperator.NOT_EQUALS:
            return column != value
        if expression.operator == FilterOperator.GREATER_THAN:
            return column > value
        if expression.operator == FilterOperator.GREATER_THAN_OR_EQUAL:
            return column >= value
        if expression.operator == FilterOperator.LESS_THAN:
            return column < value
        if expression.operator == FilterOperator.LESS_THAN_OR_EQUAL:
            return column <= value
        if expression.operator == FilterOperator.CONTAINS:
            return column.contains(value)
        if expression.operator == FilterOperator.STARTS_WITH:
            return column.startswith(value)
        if expression.operator == FilterOperator.ENDS_WITH:
            return column.endswith(value)
        if expression.operator == FilterOperator.IN:
            return column.in_(value)

        raise ValueError(f"Unsupported filter operator: {expression.operator}")

    def _primary_key_attribute(self) -> InstrumentedAttribute[Any]:
        """Return the mapped primary key attribute for the repository model."""
        mapper = cast(Mapper[Any], inspect(self.model_type))
        primary_key = mapper.primary_key[0]
        primary_key_name = cast(str, primary_key.key)
        return cast(InstrumentedAttribute[Any], getattr(self.model_type, primary_key_name))

    def _column(self, field: str) -> InstrumentedAttribute[Any]:
        """Return a mapped column by field name."""
        return cast(InstrumentedAttribute[Any], getattr(self.model_type, field))
