from __future__ import annotations

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session, selectinload

from domain.identity.entities import Role, User
from infrastructure.persistence.sqlalchemy.identity.mappers import IdentityMapper
from infrastructure.persistence.sqlalchemy.identity.models import RoleModel, UserModel
from presentation.modules.user_management.application.dto.paging import (
    Page,
    SortDirection,
    UserSearchCriteria,
    UserStatusFilter,
)
from presentation.modules.user_management.domain.repositories import IUserManagementRepository
from shared.kernel.identity import Identity


class SqlAlchemyUserManagementRepository(IUserManagementRepository):
    """SQLAlchemy implementation for user management."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def add_user(self, user: User) -> User:
        """Add a user."""
        self._session.merge(IdentityMapper.user_to_model(user))
        return user

    def update_user(self, user: User) -> User:
        """Update a user."""
        self._session.merge(IdentityMapper.user_to_model(user))
        return user

    def get_user(self, user_id: Identity) -> User | None:
        """Return a user by id."""
        model = self._session.scalars(
            select(UserModel)
            .options(selectinload(UserModel.roles))
            .where(UserModel.id == str(user_id))
        ).one_or_none()
        return IdentityMapper.user_to_domain(model) if model is not None else None

    def get_by_username(self, username: str) -> User | None:
        """Return a user by username."""
        model = self._session.scalars(
            select(UserModel)
            .options(selectinload(UserModel.roles))
            .where(UserModel.username == username)
        ).one_or_none()
        return IdentityMapper.user_to_domain(model) if model is not None else None

    def get_by_email(self, email: str) -> User | None:
        """Return a user by email."""
        model = self._session.scalars(
            select(UserModel).options(selectinload(UserModel.roles)).where(UserModel.email == email)
        ).one_or_none()
        return IdentityMapper.user_to_domain(model) if model is not None else None

    def search_users(self, criteria: UserSearchCriteria) -> Page[User]:
        """Search users with pagination."""
        statement = select(UserModel).options(selectinload(UserModel.roles))
        count_statement = select(func.count()).select_from(UserModel)
        filters = []
        term = criteria.term.strip()
        if term:
            like = f"%{term}%"
            filters.append(or_(UserModel.username.ilike(like), UserModel.email.ilike(like)))
        if criteria.status == UserStatusFilter.ACTIVE:
            filters.append(UserModel.active.is_(True))
        if criteria.status == UserStatusFilter.INACTIVE:
            filters.append(UserModel.active.is_(False))
        for item in filters:
            statement = statement.where(item)
            count_statement = count_statement.where(item)
        order_column = {
            "email": UserModel.email,
            "updated_at": UserModel.updated_at,
        }.get(criteria.sort_by, UserModel.username)
        if criteria.direction == SortDirection.DESC:
            statement = statement.order_by(order_column.desc())
        else:
            statement = statement.order_by(order_column)
        statement = statement.offset((criteria.page - 1) * criteria.page_size).limit(
            criteria.page_size
        )
        models = self._session.scalars(statement).all()
        total = self._session.execute(count_statement).scalar_one()
        return Page(
            items=tuple(IdentityMapper.user_to_domain(model) for model in models),
            total=total,
            page=criteria.page,
            page_size=criteria.page_size,
        )

    def count_active_admins(self) -> int:
        """Return active administrator count."""
        return self._session.execute(
            select(func.count())
            .select_from(UserModel)
            .join(UserModel.roles)
            .where(UserModel.active.is_(True), RoleModel.name == "admin")
        ).scalar_one()

    def get_role(self, role_id: Identity) -> Role | None:
        """Return a role by id."""
        model = self._session.get(RoleModel, str(role_id))
        return IdentityMapper.role_to_domain(model) if model is not None else None

    def list_roles(self) -> tuple[Role, ...]:
        """Return roles."""
        models = self._session.scalars(select(RoleModel)).all()
        return tuple(IdentityMapper.role_to_domain(model) for model in models)
