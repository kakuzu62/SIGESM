from __future__ import annotations

from collections.abc import Sequence

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from domain.identity.entities import Permission
from domain.identity.repositories import IPermissionRepository
from domain.identity.value_objects import PermissionCode
from infrastructure.persistence.sqlalchemy.identity.mappers import IdentityMapper
from infrastructure.persistence.sqlalchemy.identity.models import PermissionModel
from shared.kernel.identity import Identity


class SqlAlchemyPermissionRepository(IPermissionRepository):
    """SQLAlchemy repository for permissions."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, entity: Permission) -> Permission:
        """Add a permission."""
        self._session.merge(IdentityMapper.permission_to_model(entity))
        return entity

    def update(self, entity: Permission) -> Permission:
        """Update a permission."""
        self._session.merge(IdentityMapper.permission_to_model(entity))
        return entity

    def delete(self, entity: Permission) -> None:
        """Delete a permission."""
        model = self._session.get(PermissionModel, str(entity.id))
        if model is not None:
            self._session.delete(model)

    def get_by_id(self, entity_id: Identity) -> Permission | None:
        """Return a permission by identity."""
        model = self._session.get(PermissionModel, str(entity_id))
        if model is None:
            return None
        return IdentityMapper.permission_to_domain(model)

    def get_by_code(self, code: PermissionCode) -> Permission | None:
        """Return a permission by code."""
        model = self._session.scalars(
            select(PermissionModel).where(PermissionModel.code == code.value)
        ).one_or_none()
        if model is None:
            return None
        return IdentityMapper.permission_to_domain(model)

    def exists(self, entity_id: Identity) -> bool:
        """Return whether a permission exists."""
        return self._session.get(PermissionModel, str(entity_id)) is not None

    def count(self) -> int:
        """Return permission count."""
        return self._session.execute(select(func.count()).select_from(PermissionModel)).scalar_one()

    def list(self) -> Sequence[Permission]:
        """Return permissions."""
        return tuple(
            IdentityMapper.permission_to_domain(model)
            for model in self._session.scalars(select(PermissionModel)).all()
        )

    def first(self) -> Permission | None:
        """Return first permission."""
        model = self._session.scalars(select(PermissionModel).limit(1)).first()
        if model is None:
            return None
        return IdentityMapper.permission_to_domain(model)
