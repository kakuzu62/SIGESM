from __future__ import annotations

from collections.abc import Sequence

from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from domain.identity.entities import Role
from domain.identity.repositories import IRoleRepository
from infrastructure.persistence.sqlalchemy.identity.mappers import IdentityMapper
from infrastructure.persistence.sqlalchemy.identity.models import (
    PermissionModel,
    RoleModel,
    UserModel,
)
from infrastructure.persistence.sqlalchemy.identity.models.user_model import identity_user_roles
from shared.kernel.identity import Identity


class SqlAlchemyRoleRepository(IRoleRepository):
    """SQLAlchemy repository for roles."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, entity: Role) -> Role:
        """Add a role."""
        self._session.merge(self._to_model(entity))
        return entity

    def update(self, entity: Role) -> Role:
        """Update a role."""
        self._session.merge(self._to_model(entity))
        return entity

    def delete(self, entity: Role) -> None:
        """Delete a role."""
        model = self._session.get(RoleModel, str(entity.id))
        if model is not None:
            self._session.delete(model)

    def get_by_id(self, entity_id: Identity) -> Role | None:
        """Return a role by identity."""
        model = self._session.scalars(
            select(RoleModel)
            .options(selectinload(RoleModel.permissions))
            .where(RoleModel.id == str(entity_id))
        ).one_or_none()
        if model is None:
            return None
        return IdentityMapper.role_to_domain(model)

    def _to_model(self, entity: Role) -> RoleModel:
        """Map a role using already persisted permissions when available."""
        model = IdentityMapper.role_to_model(entity)
        model.permissions = [
            self._session.get(PermissionModel, str(permission.id))
            or IdentityMapper.permission_to_model(permission)
            for permission in entity.permissions
        ]
        return model

    def get_by_name(self, name: str) -> Role | None:
        """Return a role by name."""
        model = self._session.scalars(
            select(RoleModel)
            .options(selectinload(RoleModel.permissions))
            .where(RoleModel.normalized_name == Role.normalize_name(name))
        ).one_or_none()
        if model is None:
            return None
        return IdentityMapper.role_to_domain(model)

    def exists(self, entity_id: Identity) -> bool:
        """Return whether a role exists."""
        return self._session.get(RoleModel, str(entity_id)) is not None

    def get_by_ids(self, role_ids: Sequence[Identity]) -> tuple[Role, ...]:
        """Return roles matching the provided identities."""
        ids = [str(role_id) for role_id in role_ids]
        if not ids:
            return ()
        models = self._session.scalars(
            select(RoleModel)
            .options(selectinload(RoleModel.permissions))
            .where(RoleModel.id.in_(ids))
            .order_by(RoleModel.name)
        ).all()
        return tuple(IdentityMapper.role_to_domain(model) for model in models)

    def list_active(self) -> tuple[Role, ...]:
        """Return active roles available for assignment."""
        models = self._session.scalars(
            select(RoleModel)
            .options(selectinload(RoleModel.permissions))
            .where(RoleModel.active.is_(True))
            .order_by(RoleModel.name)
        ).all()
        return tuple(IdentityMapper.role_to_domain(model) for model in models)

    def count_active_users_with_role(self, role_id: Identity) -> int:
        """Return active user count assigned to the role."""
        return self._session.execute(
            select(func.count())
            .select_from(identity_user_roles.join(UserModel))
            .where(
                identity_user_roles.c.role_id == str(role_id),
                UserModel.active.is_(True),
            )
        ).scalar_one()

    def count(self) -> int:
        """Return role count."""
        return self._session.execute(select(func.count()).select_from(RoleModel)).scalar_one()

    def list(self) -> Sequence[Role]:
        """Return roles."""
        models = self._session.scalars(
            select(RoleModel).options(selectinload(RoleModel.permissions))
        ).all()
        return tuple(IdentityMapper.role_to_domain(model) for model in models)

    def first(self) -> Role | None:
        """Return first role."""
        model = self._session.scalars(
            select(RoleModel).options(selectinload(RoleModel.permissions)).limit(1)
        ).first()
        if model is None:
            return None
        return IdentityMapper.role_to_domain(model)
