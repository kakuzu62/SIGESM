from __future__ import annotations

from collections.abc import Sequence

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from domain.identity.entities import PasswordResetRequest
from domain.identity.repositories import IPasswordResetRequestRepository
from infrastructure.persistence.sqlalchemy.identity.mappers import IdentityMapper
from infrastructure.persistence.sqlalchemy.identity.models import PasswordResetRequestModel
from shared.kernel.identity import Identity


class SqlAlchemyPasswordResetRequestRepository(IPasswordResetRequestRepository):
    """SQLAlchemy repository for password reset requests."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, entity: PasswordResetRequest) -> PasswordResetRequest:
        """Add a password reset request."""
        self._session.merge(IdentityMapper.password_reset_to_model(entity))
        return entity

    def update(self, entity: PasswordResetRequest) -> PasswordResetRequest:
        """Update a password reset request."""
        self._session.merge(IdentityMapper.password_reset_to_model(entity))
        return entity

    def delete(self, entity: PasswordResetRequest) -> None:
        """Delete a password reset request."""
        model = self._session.get(PasswordResetRequestModel, str(entity.id))
        if model is not None:
            self._session.delete(model)

    def get_by_id(self, entity_id: Identity) -> PasswordResetRequest | None:
        """Return a password reset request by identity."""
        model = self._session.get(PasswordResetRequestModel, str(entity_id))
        if model is None:
            return None
        return IdentityMapper.password_reset_to_domain(model)

    def get_by_token_hash(self, token_hash: str) -> PasswordResetRequest | None:
        """Return a password reset request by token hash."""
        model = self._session.scalars(
            select(PasswordResetRequestModel).where(
                PasswordResetRequestModel.token_hash == token_hash
            )
        ).one_or_none()
        if model is None:
            return None
        return IdentityMapper.password_reset_to_domain(model)

    def get_active_by_user(self, user_id: Identity) -> PasswordResetRequest | None:
        """Return active password reset request for a user."""
        model = self._session.scalars(
            select(PasswordResetRequestModel).where(
                PasswordResetRequestModel.user_id == str(user_id),
                PasswordResetRequestModel.used_at.is_(None),
            )
        ).first()
        if model is None:
            return None
        return IdentityMapper.password_reset_to_domain(model)

    def exists(self, entity_id: Identity) -> bool:
        """Return whether a password reset request exists."""
        return self._session.get(PasswordResetRequestModel, str(entity_id)) is not None

    def count(self) -> int:
        """Return password reset request count."""
        return self._session.execute(
            select(func.count()).select_from(PasswordResetRequestModel)
        ).scalar_one()

    def list(self) -> Sequence[PasswordResetRequest]:
        """Return password reset requests."""
        return tuple(
            IdentityMapper.password_reset_to_domain(model)
            for model in self._session.scalars(select(PasswordResetRequestModel)).all()
        )

    def first(self) -> PasswordResetRequest | None:
        """Return first password reset request."""
        model = self._session.scalars(select(PasswordResetRequestModel).limit(1)).first()
        if model is None:
            return None
        return IdentityMapper.password_reset_to_domain(model)
