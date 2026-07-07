from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path

import pytest

from core.config.settings import DatabaseSettings
from core.database.base import Base
from core.database.engine import DatabaseEngineFactory
from core.database.session import DatabaseSessionFactory
from domain.identity.entities import Permission, Role, User
from domain.identity.services import PasswordService
from domain.identity.value_objects import Email, PermissionCode, Username
from infrastructure.persistence.sqlalchemy.identity.models import (
    PermissionModel,
    RoleModel,
    UserModel,
    UserSessionModel,
)
from infrastructure.persistence.sqlalchemy.identity.repositories import (
    SqlAlchemyPermissionRepository,
    SqlAlchemyRoleRepository,
    SqlAlchemyUserRepository,
)
from infrastructure.persistence.sqlalchemy.session_context import SessionContext


@pytest.fixture
def identity_session_factory(tmp_path: Path) -> Iterator[DatabaseSessionFactory]:
    """Create an isolated database with identity tables."""
    _ = (PermissionModel, RoleModel, UserModel, UserSessionModel)
    database_settings = DatabaseSettings(database=str(tmp_path / "identity.db"))
    factory = DatabaseSessionFactory.from_engine_factory(DatabaseEngineFactory(database_settings))
    Base.metadata.create_all(factory.engine)
    yield factory
    Base.metadata.drop_all(factory.engine)


def test_identity_repositories_persist_user_roles_and_permissions(
    identity_session_factory: DatabaseSessionFactory,
) -> None:
    permission = Permission.create(PermissionCode("IDENTITY.USER.CREATE"), "Create users")
    role = Role.create("Administrator", "System administrators")
    role.add_permission(permission)
    user = User.create(
        Username("admin"),
        Email("admin@sigesm.local"),
        PasswordService().hash_password("Strong#123"),
    )
    user.assign_role(role)

    with SessionContext(identity_session_factory) as session:
        user_repository = SqlAlchemyUserRepository(session)
        user_repository.add(user)
        session.commit()

    with SessionContext(identity_session_factory) as session:
        user_repository = SqlAlchemyUserRepository(session)
        role_repository = SqlAlchemyRoleRepository(session)
        permission_repository = SqlAlchemyPermissionRepository(session)

        persisted_user = user_repository.get_by_username(Username("admin"))
        persisted_role = role_repository.get_by_name("Administrator")
        persisted_permission = permission_repository.get_by_code(
            PermissionCode("identity:user:create")
        )

        assert persisted_user is not None
        assert persisted_role is not None
        assert persisted_permission is not None
        assert persisted_user.email.value == "admin@sigesm.local"
        assert persisted_user.roles[0].permissions[0].code.value == "IDENTITY.USER.CREATE"
        assert user_repository.count() == 1
        assert role_repository.count() == 1
        assert permission_repository.count() == 1
