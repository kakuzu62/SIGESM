from __future__ import annotations

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session, selectinload

from infrastructure.persistence.sqlalchemy.identity.models import UserModel
from presentation.modules.user_management.application.common import PagedResult, SortDirection
from presentation.modules.user_management.application.queries.list_users import (
    ListUsersQuery,
    UserListItemDTO,
)
from presentation.modules.user_management.domain.repositories import IUserListingRepository


class SqlAlchemyUserListingRepository(IUserListingRepository):
    """SQLAlchemy read repository for user listing."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def list_users(self, query: ListUsersQuery) -> PagedResult[UserListItemDTO]:
        """Return a paged user list."""
        return self.paginate(query)

    def search(self, query: ListUsersQuery) -> PagedResult[UserListItemDTO]:
        """Search users."""
        return self.paginate(query)

    def order(self, query: ListUsersQuery) -> PagedResult[UserListItemDTO]:
        """Order users."""
        return self.paginate(query)

    def paginate(self, query: ListUsersQuery) -> PagedResult[UserListItemDTO]:
        """Paginate users using SQL."""
        statement = select(UserModel).options(selectinload(UserModel.roles))
        count_statement = select(func.count()).select_from(UserModel)
        term = query.filter_text.strip()
        if term:
            like = f"%{term}%"
            predicate = or_(UserModel.username.ilike(like), UserModel.email.ilike(like))
            statement = statement.where(predicate)
            count_statement = count_statement.where(predicate)
        order_column = {
            "email": UserModel.email,
            "status": UserModel.active,
            "created_at": UserModel.created_at,
        }.get(query.sort_by, UserModel.username)
        statement = statement.order_by(
            order_column.desc() if query.direction == SortDirection.DESC else order_column
        )
        statement = statement.offset((query.page - 1) * query.page_size).limit(query.page_size)
        models = self._session.scalars(statement).all()
        total = self._session.execute(count_statement).scalar_one()
        return PagedResult(
            items=tuple(
                UserListItemDTO(
                    id=model.id,
                    login=model.username,
                    name=model.username,
                    email=model.email,
                    status="Ativo" if model.active else "Inativo",
                    profiles=tuple(role.name for role in model.roles),
                    last_access_at=None,
                    created_at=model.created_at,
                )
                for model in models
            ),
            total=total,
            page=query.page,
            page_size=query.page_size,
        )

    def total(self, query: ListUsersQuery) -> int:
        """Return total rows for a query."""
        return self.paginate(
            ListUsersQuery(
                page=1,
                page_size=1,
                sort_by=query.sort_by,
                direction=query.direction,
                filter_text=query.filter_text,
            )
        ).total
