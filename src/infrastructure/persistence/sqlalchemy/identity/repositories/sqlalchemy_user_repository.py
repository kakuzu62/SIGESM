from __future__ import annotations

from collections.abc import Sequence

from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from domain.identity.entities import User
from domain.identity.repositories import IUserRepository
from domain.identity.value_objects import Email, Username
from infrastructure.persistence.sqlalchemy.identity.mappers import IdentityMapper
from infrastructure.persistence.sqlalchemy.identity.models import RoleModel, UserModel
from shared.kernel.identity import Identity


class SqlAlchemyUserRepository(IUserRepository):
    """SQLAlchemy repository for users."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, entity: User) -> User:
        """Add a user."""
        self._session.merge(self._to_model(entity))
        return entity

    def update(self, entity: User) -> User:
        """Update a user."""
        model = self._session.get(UserModel, str(entity.id))
        if model is None:
            self._session.merge(self._to_model(entity))
            return entity

        model.full_name = entity.full_name
        model.username = entity.username.value
        model.email = entity.email.value
        model.password_hash = entity.password_hash.value
        model.active = entity.active
        model.failed_login_attempts = entity.failed_login_attempts
        model.locked_until = entity.locked_until
        model.created_at = entity.created_at
        model.updated_at = entity.updated_at
        model.roles = [
            self._session.get(RoleModel, str(role.id)) or IdentityMapper.role_to_model(role)
            for role in entity.roles
        ]
        return entity

    def delete(self, entity: User) -> None:
        """Delete a user."""
        model = self._session.get(UserModel, str(entity.id))
        if model is not None:
            self._session.delete(model)

    def get_by_id(self, entity_id: Identity) -> User | None:
        """Return a user by identity."""
        model = self._session.scalars(
            select(UserModel)
            .options(selectinload(UserModel.roles))
            .where(UserModel.id == str(entity_id))
        ).one_or_none()
        if model is None:
            return None
        return IdentityMapper.user_to_domain(model)

    def _to_model(self, entity: User) -> UserModel:
        """Map a user using already persisted roles when available."""
        model = IdentityMapper.user_to_model(entity)
        model.roles = [
            self._session.get(RoleModel, str(role.id)) or IdentityMapper.role_to_model(role)
            for role in entity.roles
        ]
        return model

    def get_by_username(self, username: Username) -> User | None:
        """Return a user by username."""
        model = self._session.scalars(
            select(UserModel)
            .options(selectinload(UserModel.roles))
            .where(UserModel.username == username.value)
        ).one_or_none()
        if model is None:
            return None
        return IdentityMapper.user_to_domain(model)

    def get_by_email(self, email: Email) -> User | None:
        """Return a user by email."""
        model = self._session.scalars(
            select(UserModel)
            .options(selectinload(UserModel.roles))
            .where(UserModel.email == email.value)
        ).one_or_none()
        if model is None:
            return None
        return IdentityMapper.user_to_domain(model)

    def exists(self, entity_id: Identity) -> bool:
        """Return whether a user exists."""
        return self._session.get(UserModel, str(entity_id)) is not None

    def count(self) -> int:
        """Return user count."""
        return self._session.execute(select(func.count()).select_from(UserModel)).scalar_one()

    def list(self) -> Sequence[User]:
        """Return users."""
        models = self._session.scalars(
            select(UserModel).options(selectinload(UserModel.roles))
        ).all()
        return tuple(IdentityMapper.user_to_domain(model) for model in models)

    def first(self) -> User | None:
        """Return first user."""
        model = self._session.scalars(
            select(UserModel).options(selectinload(UserModel.roles)).limit(1)
        ).first()
        if model is None:
            return None
        return IdentityMapper.user_to_domain(model)
