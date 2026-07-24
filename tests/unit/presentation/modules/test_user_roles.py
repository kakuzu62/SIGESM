from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path
from types import TracebackType

import pytest
from PySide6.QtWidgets import QApplication

from core.config.settings import DatabaseSettings
from core.database.base import Base
from core.database.engine import DatabaseEngineFactory
from core.database.session import DatabaseSessionFactory
from domain.identity.entities import Role, User
from domain.identity.repositories import IRoleRepository, IUserRepository
from domain.identity.value_objects import Email, PasswordHash, Username
from infrastructure.identity import InMemoryRoleRepository, InMemoryUserRepository
from infrastructure.persistence.sqlalchemy.identity.models import RoleModel, UserModel
from infrastructure.persistence.sqlalchemy.identity.repositories import (
    SqlAlchemyRoleRepository,
    SqlAlchemyUserRepository,
)
from presentation.modules.user_management.application import (
    AssignUserRolesService,
    ListAvailableRolesService,
    UserListingService,
)
from presentation.modules.user_management.application.commands.assign_user_roles import (
    AssignUserRolesCommand,
    AssignUserRolesHandler,
)
from presentation.modules.user_management.application.commands.assign_user_roles.unit_of_work import (
    UserRolesPersistenceError,
    UserRolesUnitOfWork,
    UserRolesUnitOfWorkFactory,
)
from presentation.modules.user_management.application.commands.assign_user_roles.validator import (
    AssignUserRolesCommandValidator,
)
from presentation.modules.user_management.application.queries.list_available_roles import (
    ListAvailableRolesQuery,
)
from presentation.modules.user_management.application.queries.list_users import (
    ListUsersQuery,
    UserListItemDTO,
)
from presentation.modules.user_management.infrastructure.persistence import (
    SqlAlchemyUserRolesUnitOfWorkFactory,
)
from presentation.modules.user_management.infrastructure.repositories import (
    InMemoryUserListingRepository,
    InMemoryUserRolesUnitOfWorkFactory,
)
from presentation.modules.user_management.presentation.dialogs import UserRolesDialog
from presentation.modules.user_management.presentation.viewmodels import UserRolesViewModel
from shared.kernel.identity import Identity

_VALID_ARGON2ID_HASH = (
    "$argon2id$v=19$m=65536,t=3,p=4$"
    "c2lnZXNtX3Rlc3Rfc2FsdA$"
    "F5agQp7LdbYQlwU++q7RrA3y8nY5jD9O81jHT2e66eE"
)


class _ConflictOnCommitUnitOfWork(UserRolesUnitOfWork):
    def __init__(self, users: IUserRepository, roles: IRoleRepository) -> None:
        self._users = users
        self._roles = roles
        self.rollbacks = 0

    @property
    def users(self) -> IUserRepository:
        return self._users

    @property
    def roles(self) -> IRoleRepository:
        return self._roles

    def __enter__(self) -> _ConflictOnCommitUnitOfWork:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        if exc_type is not None:
            self.rollback()

    def commit(self) -> None:
        raise UserRolesPersistenceError("conflict")

    def rollback(self) -> None:
        self.rollbacks += 1


class _ConflictOnCommitFactory(UserRolesUnitOfWorkFactory):
    def __init__(self, users: IUserRepository, roles: IRoleRepository) -> None:
        self.unit_of_work = _ConflictOnCommitUnitOfWork(users, roles)

    def create(self) -> _ConflictOnCommitUnitOfWork:
        return self.unit_of_work


@pytest.fixture
def qt_app() -> QApplication:
    """Return a QApplication for widget tests."""
    application = QApplication.instance()
    if isinstance(application, QApplication):
        return application
    return QApplication([])


@pytest.fixture
def identity_session_factory(tmp_path: Path) -> Iterator[DatabaseSessionFactory]:
    """Create an isolated identity database."""
    database_settings = DatabaseSettings(database=str(tmp_path / "identity_roles.db"))
    factory = DatabaseSessionFactory.from_engine_factory(DatabaseEngineFactory(database_settings))
    _ = (RoleModel, UserModel)
    Base.metadata.create_all(factory.engine)
    yield factory
    Base.metadata.drop_all(factory.engine)


def test_user_set_roles_assigns_removes_and_preserves_invariants() -> None:
    user = _user("manager", "manager@sigesm.local", "Manager User")
    admin = Role.create("Administrador")
    operator = Role.create("Operador")
    original_id = user.id
    original_hash = user.password_hash
    original_created_at = user.created_at
    original_updated_at = user.updated_at

    user.set_roles((admin, operator, admin))

    assert tuple(role.name for role in user.roles) == ("Administrador", "Operador")
    assert user.updated_at >= original_updated_at
    assert user.id == original_id
    assert user.password_hash == original_hash
    assert user.created_at == original_created_at

    updated_at = user.updated_at
    user.set_roles((admin, operator))

    assert user.updated_at == updated_at

    user.set_roles((operator,))

    assert tuple(role.name for role in user.roles) == ("Operador",)


def test_assign_user_roles_validator_rejects_invalid_and_duplicate_ids() -> None:
    validator = AssignUserRolesCommandValidator()
    user_id = str(Identity.new())
    role_id = str(Identity.new())

    assert validator.validate(AssignUserRolesCommand("", user_id, (role_id,))).is_failure
    assert validator.validate(AssignUserRolesCommand(user_id, "", (role_id,))).is_failure
    assert validator.validate(AssignUserRolesCommand(user_id, user_id, ("bad",))).is_failure
    assert validator.validate(
        AssignUserRolesCommand(user_id, user_id, (role_id, role_id))
    ).is_failure
    assert validator.validate(AssignUserRolesCommand(user_id, user_id, ())).is_success


def test_assign_user_roles_handler_assigns_replaces_and_commits() -> None:
    users, roles, actor, target, admin, operator, _consulta = _identity_data()
    factory = InMemoryUserRolesUnitOfWorkFactory(users, roles)

    assigned = AssignUserRolesHandler(factory).handle(
        AssignUserRolesCommand(str(actor.id), str(target.id), (str(operator.id),))
    )
    replaced = AssignUserRolesHandler(factory).handle(
        AssignUserRolesCommand(
            str(actor.id),
            str(target.id),
            (str(admin.id), str(operator.id)),
        )
    )

    assert assigned.is_success
    assert replaced.is_success
    assert replaced.value.roles == ("Administrador", "Operador")
    assert not hasattr(replaced.value, "password")
    assert not hasattr(replaced.value, "password_hash")
    assert factory.created[0].commits == 1
    assert factory.created[1].commits == 1


def test_assign_user_roles_handler_rejects_missing_user_missing_role_and_inactive_role() -> None:
    users, roles, actor, _target, _admin, _operator, consulta = _identity_data()
    consulta.deactivate()
    factory = InMemoryUserRolesUnitOfWorkFactory(users, roles)

    missing_user = AssignUserRolesHandler(factory).handle(
        AssignUserRolesCommand(str(actor.id), str(Identity.new()), ())
    )
    missing_role = AssignUserRolesHandler(factory).handle(
        AssignUserRolesCommand(str(actor.id), str(actor.id), (str(Identity.new()),))
    )
    inactive_role = AssignUserRolesHandler(factory).handle(
        AssignUserRolesCommand(str(actor.id), str(actor.id), (str(consulta.id),))
    )

    assert missing_user.is_failure
    assert missing_user.error == "Usuario nao encontrado."
    assert missing_role.is_failure
    assert missing_role.error == "Um ou mais perfis nao foram encontrados."
    assert inactive_role.is_failure
    assert inactive_role.error == "Perfis inativos nao podem ser atribuidos."
    assert factory.created[0].rollbacks == 1
    assert factory.created[1].rollbacks == 1
    assert factory.created[2].rollbacks == 1


def test_assign_user_roles_handler_protects_last_active_administrator() -> None:
    users, roles, actor, target, admin, operator, _consulta = _identity_data()
    actor.set_roles((admin,))
    target.set_roles((operator,))
    users.update(actor)
    users.update(target)

    result = AssignUserRolesHandler(InMemoryUserRolesUnitOfWorkFactory(users, roles)).handle(
        AssignUserRolesCommand(str(actor.id), str(actor.id), (str(operator.id),))
    )

    assert result.is_failure
    assert result.error == "O sistema deve manter ao menos um administrador ativo."
    assert users.get_by_id(actor.id) is not None
    assert any(role.id == admin.id for role in actor.roles)


def test_assign_user_roles_handler_allows_self_change_when_another_admin_exists() -> None:
    users, roles, actor, target, admin, operator, _consulta = _identity_data()
    actor.set_roles((admin,))
    target.set_roles((admin,))
    users.update(actor)
    users.update(target)

    result = AssignUserRolesHandler(InMemoryUserRolesUnitOfWorkFactory(users, roles)).handle(
        AssignUserRolesCommand(str(actor.id), str(actor.id), (str(operator.id),))
    )

    assert result.is_success
    assert result.value.roles == ("Operador",)


def test_assign_user_roles_handler_rolls_back_persistence_error() -> None:
    users, roles, actor, target, _admin, operator, _consulta = _identity_data()
    factory = _ConflictOnCommitFactory(users, roles)

    result = AssignUserRolesHandler(factory).handle(
        AssignUserRolesCommand(str(actor.id), str(target.id), (str(operator.id),))
    )

    assert result.is_failure
    assert result.error == "Nao foi possivel atualizar os perfis do usuario."
    assert factory.unit_of_work.rollbacks == 1


def test_list_available_roles_returns_only_active_sorted_roles() -> None:
    _users, roles, _actor, _target, _admin, _operator, consulta = _identity_data()
    consulta.deactivate()

    result = ListAvailableRolesService(roles).list_roles(ListAvailableRolesQuery())

    assert result.is_success
    assert tuple(role.name for role in result.value) == ("Administrador", "Operador")
    assert not hasattr(result.value[0], "permissions")


def test_user_roles_view_model_loads_marks_changes_and_submits(qt_app: QApplication) -> None:
    users, roles, actor, target, _admin, operator, _consulta = _identity_data()
    target.set_roles((operator,))
    users.update(target)
    item = _listing_item(users, target.id)
    view_model = UserRolesViewModel(
        str(actor.id),
        item,
        ListAvailableRolesService(roles),
        AssignUserRolesService(InMemoryUserRolesUnitOfWorkFactory(users, roles)),
    )
    emitted: list[object] = []
    view_model.roles_updated.connect(lambda user: emitted.append(user))

    view_model.load()

    assert str(operator.id) in view_model.selected_role_ids
    assert not view_model.has_changes
    assert not view_model.can_submit

    view_model.set_role_selected(str(operator.id), False)

    assert view_model.has_changes
    assert view_model.can_submit
    view_model.submit()

    assert len(emitted) == 1
    assert not view_model.is_loading
    assert users.get_by_id(target.id) is not None
    assert users.get_by_id(target.id).roles == ()
    qt_app.processEvents()


def test_user_roles_view_model_preserves_selection_on_failure(qt_app: QApplication) -> None:
    users, roles, actor, target, admin, operator, _consulta = _identity_data()
    actor.set_roles((admin,))
    users.update(actor)
    view_model = UserRolesViewModel(
        str(actor.id),
        _listing_item(users, actor.id),
        ListAvailableRolesService(roles),
        AssignUserRolesService(InMemoryUserRolesUnitOfWorkFactory(users, roles)),
    )
    failures: list[str] = []
    view_model.update_failed.connect(failures.append)

    view_model.load()
    view_model.set_role_selected(str(admin.id), False)
    view_model.set_role_selected(str(operator.id), True)
    view_model.submit()

    assert failures == ["O sistema deve manter ao menos um administrador ativo."]
    assert str(operator.id) in view_model.selected_role_ids
    assert str(admin.id) not in view_model.selected_role_ids
    qt_app.processEvents()


def test_user_roles_dialog_renders_checkboxes_and_cancel_does_not_persist(
    qt_app: QApplication,
) -> None:
    users, roles, actor, target, _admin, operator, _consulta = _identity_data()
    target.set_roles((operator,))
    users.update(target)
    factory = InMemoryUserRolesUnitOfWorkFactory(users, roles)
    dialog = UserRolesDialog(
        UserRolesViewModel(
            str(actor.id),
            _listing_item(users, target.id),
            ListAvailableRolesService(roles),
            AssignUserRolesService(factory),
        )
    )

    assert dialog.windowTitle() == "Gerenciar perfis"
    assert str(operator.id) in dialog._checkboxes
    assert dialog._checkboxes[str(operator.id)].isChecked()
    assert not dialog._save_button.isEnabled()
    dialog.reject()

    assert factory.created == []
    qt_app.processEvents()


def test_sqlalchemy_user_roles_persist_assignment_and_removal(
    identity_session_factory: DatabaseSessionFactory,
) -> None:
    with identity_session_factory.context() as session:
        users = SqlAlchemyUserRepository(session)
        roles = SqlAlchemyRoleRepository(session)
        actor = _user("actor", "actor@sigesm.local", "Actor User")
        target = _user("target", "target@sigesm.local", "Target User")
        admin = Role.create("Administrador")
        operator = Role.create("Operador")
        users.add(actor)
        users.add(target)
        roles.add(admin)
        roles.add(operator)
        session.commit()
        actor_id = str(actor.id)
        target_id = str(target.id)
        operator_id = str(operator.id)

    service = AssignUserRolesService(SqlAlchemyUserRolesUnitOfWorkFactory(identity_session_factory))
    assigned = service.assign_roles(AssignUserRolesCommand(actor_id, target_id, (operator_id,)))
    removed = service.assign_roles(AssignUserRolesCommand(actor_id, target_id, ()))

    assert assigned.is_success
    assert removed.is_success
    with identity_session_factory.context() as session:
        users = SqlAlchemyUserRepository(session)
        persisted = users.get_by_id(Identity.from_string(target_id))
        assert persisted is not None
        assert persisted.roles == ()


def _identity_data() -> tuple[
    InMemoryUserRepository,
    InMemoryRoleRepository,
    User,
    User,
    Role,
    Role,
    Role,
]:
    users = InMemoryUserRepository()
    roles = InMemoryRoleRepository(users)
    actor = _user("actor", "actor@sigesm.local", "Actor User")
    target = _user("target", "target@sigesm.local", "Target User")
    admin = Role.create("Administrador")
    operator = Role.create("Operador")
    consulta = Role.create("Consulta")
    roles.add(admin)
    roles.add(operator)
    roles.add(consulta)
    users.add(actor)
    users.add(target)
    return users, roles, actor, target, admin, operator, consulta


def _user(username: str, email: str, full_name: str) -> User:
    return User.create(
        Username(username),
        Email(email),
        PasswordHash(_VALID_ARGON2ID_HASH),
        full_name=full_name,
    )


def _listing_item(users: IUserRepository, user_id: Identity) -> UserListItemDTO:
    result = UserListingService(InMemoryUserListingRepository(users)).list_users(ListUsersQuery())
    assert result.is_success
    return next(item for item in result.value.items if item.id == str(user_id))
