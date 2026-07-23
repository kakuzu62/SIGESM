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
from domain.identity.entities import User
from domain.identity.repositories import IUserRepository
from domain.identity.value_objects import Email, PasswordHash, Username
from infrastructure.identity import InMemoryUserRepository
from infrastructure.persistence.sqlalchemy.identity.models import UserModel
from infrastructure.persistence.sqlalchemy.identity.repositories import SqlAlchemyUserRepository
from presentation.modules.user_management.application import EditUserService, UserListingService
from presentation.modules.user_management.application.commands.update_user import (
    UpdateUserCommand,
    UpdateUserHandler,
)
from presentation.modules.user_management.application.commands.update_user.unit_of_work import (
    UserUpdateConflictError,
    UserUpdateUnitOfWork,
    UserUpdateUnitOfWorkFactory,
)
from presentation.modules.user_management.application.commands.update_user.validator import (
    UpdateUserCommandValidator,
)
from presentation.modules.user_management.application.queries.list_users import (
    ListUsersQuery,
    UserListItemDTO,
)
from presentation.modules.user_management.infrastructure.persistence import (
    SqlAlchemyUserUpdateUnitOfWorkFactory,
)
from presentation.modules.user_management.infrastructure.repositories import (
    InMemoryUserListingRepository,
    InMemoryUserUpdateUnitOfWorkFactory,
)
from presentation.modules.user_management.presentation.dialogs import UserFormDialog
from presentation.modules.user_management.presentation.viewmodels import EditUserViewModel
from shared.kernel.identity import Identity

_VALID_ARGON2ID_HASH = (
    "$argon2id$v=19$m=65536,t=3,p=4$"
    "c2lnZXNtX3Rlc3Rfc2FsdA$"
    "F5agQp7LdbYQlwU++q7RrA3y8nY5jD9O81jHT2e66eE"
)


class _ConflictOnCommitUnitOfWork(UserUpdateUnitOfWork):
    def __init__(self, users: IUserRepository) -> None:
        self._users = users
        self.rollbacks = 0

    @property
    def users(self) -> IUserRepository:
        return self._users

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
        raise UserUpdateConflictError("conflict")

    def rollback(self) -> None:
        self.rollbacks += 1


class _ConflictOnCommitFactory(UserUpdateUnitOfWorkFactory):
    def __init__(self, users: IUserRepository) -> None:
        self.unit_of_work = _ConflictOnCommitUnitOfWork(users)

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
    database_settings = DatabaseSettings(database=str(tmp_path / "identity_editing.db"))
    factory = DatabaseSessionFactory.from_engine_factory(DatabaseEngineFactory(database_settings))
    _ = UserModel
    Base.metadata.create_all(factory.engine)
    yield factory
    Base.metadata.drop_all(factory.engine)


def test_user_update_profile_preserves_protected_fields() -> None:
    user = _user("manager", "manager@sigesm.local", "Manager User")
    original_id = user.id
    original_hash = user.password_hash
    original_active = user.active
    original_roles = user.roles
    original_created_at = user.created_at
    original_updated_at = user.updated_at

    user.update_profile(
        "Updated Manager",
        Username("updated.manager"),
        Email("updated.manager@sigesm.local"),
    )

    assert user.id == original_id
    assert user.password_hash == original_hash
    assert user.active == original_active
    assert user.roles == original_roles
    assert user.created_at == original_created_at
    assert user.updated_at >= original_updated_at
    assert user.full_name == "Updated Manager"
    assert user.username.value == "updated.manager"
    assert user.email.value == "updated.manager@sigesm.local"


def test_update_user_validator_rejects_invalid_input_and_normalizes() -> None:
    user_id = str(Identity.new())
    validator = UpdateUserCommandValidator()

    assert validator.validate(
        UpdateUserCommand("invalid", "User", "user", "u@sigesm.local")
    ).is_failure
    assert validator.validate(UpdateUserCommand(user_id, " ", "user", "u@sigesm.local")).is_failure
    assert validator.validate(UpdateUserCommand(user_id, "User", " ", "u@sigesm.local")).is_failure
    assert validator.validate(UpdateUserCommand(user_id, "User", "user", " ")).is_failure
    assert validator.validate(
        UpdateUserCommand(user_id, "A" * 121, "user", "u@sigesm.local")
    ).is_failure

    result = validator.validate(
        UpdateUserCommand(user_id, "  User   Name  ", "  Admin.User  ", "  ADMIN@SIGESM.LOCAL  ")
    )

    assert result.is_success
    assert result.value.full_name == "User Name"
    assert result.value.username == "Admin.User"
    assert result.value.email == "ADMIN@SIGESM.LOCAL"


def test_update_user_handler_updates_and_commits() -> None:
    users = InMemoryUserRepository()
    user = _user("manager", "manager@sigesm.local", "Manager User")
    users.add(user)
    factory = InMemoryUserUpdateUnitOfWorkFactory(users)

    result = UpdateUserHandler(factory).handle(
        UpdateUserCommand(
            str(user.id),
            "Updated Manager",
            "updated.manager",
            "updated.manager@sigesm.local",
        )
    )

    assert result.is_success
    assert result.value.full_name == "Updated Manager"
    assert result.value.username == "updated.manager"
    assert not hasattr(result.value, "password")
    assert not hasattr(result.value, "password_hash")
    assert factory.created[0].commits == 1
    assert factory.created[0].rollbacks == 0
    updated = users.get_by_id(user.id)
    assert updated is not None
    assert updated.full_name == "Updated Manager"


def test_update_user_handler_rejects_missing_user_and_rolls_back() -> None:
    factory = InMemoryUserUpdateUnitOfWorkFactory(InMemoryUserRepository())

    result = UpdateUserHandler(factory).handle(
        UpdateUserCommand(str(Identity.new()), "User", "user", "user@sigesm.local")
    )

    assert result.is_failure
    assert result.error == "Usuario nao encontrado."
    assert factory.created[0].rollbacks == 1


def test_update_user_handler_rejects_duplicate_username_and_email() -> None:
    users = InMemoryUserRepository()
    user = _user("manager", "manager@sigesm.local", "Manager User")
    other = _user("other", "other@sigesm.local", "Other User")
    users.add(user)
    users.add(other)
    factory = InMemoryUserUpdateUnitOfWorkFactory(users)

    duplicate_login = UpdateUserHandler(factory).handle(
        UpdateUserCommand(str(user.id), "Manager User", "other", "manager@sigesm.local")
    )
    duplicate_email = UpdateUserHandler(factory).handle(
        UpdateUserCommand(str(user.id), "Manager User", "manager", "other@sigesm.local")
    )

    assert duplicate_login.is_failure
    assert duplicate_login.error == "Este login ja esta em uso."
    assert duplicate_email.is_failure
    assert duplicate_email.error == "Este e-mail ja esta em uso."
    assert factory.created[0].rollbacks == 1
    assert factory.created[1].rollbacks == 1


def test_update_user_handler_allows_same_username_and_email() -> None:
    users = InMemoryUserRepository()
    user = _user("manager", "manager@sigesm.local", "Manager User")
    users.add(user)

    result = UpdateUserHandler(InMemoryUserUpdateUnitOfWorkFactory(users)).handle(
        UpdateUserCommand(str(user.id), "Manager Updated", "manager", "manager@sigesm.local")
    )

    assert result.is_success
    assert result.value.full_name == "Manager Updated"


def test_update_user_handler_rolls_back_commit_conflict() -> None:
    users = InMemoryUserRepository()
    user = _user("manager", "manager@sigesm.local", "Manager User")
    users.add(user)
    factory = _ConflictOnCommitFactory(users)

    result = UpdateUserHandler(factory).handle(
        UpdateUserCommand(str(user.id), "Manager Updated", "manager2", "manager2@sigesm.local")
    )

    assert result.is_failure
    assert result.error == "Este login ou e-mail ja esta em uso."
    assert factory.unit_of_work.rollbacks == 1


def test_edit_user_view_model_tracks_changes_and_submits() -> None:
    users = InMemoryUserRepository()
    user = _user("manager", "manager@sigesm.local", "Manager User")
    users.add(user)
    item = _listing_item(users)
    view_model = EditUserViewModel(
        item,
        EditUserService(InMemoryUserUpdateUnitOfWorkFactory(users)),
    )
    emitted: list[object] = []
    view_model.user_updated.connect(lambda updated: emitted.append(updated))

    assert not view_model.has_changes
    assert not view_model.can_submit

    view_model.update_input("full_name", "Manager Updated")

    assert view_model.has_changes
    assert view_model.can_submit

    view_model.submit()

    assert len(emitted) == 1
    assert not view_model.is_loading
    updated = users.get_by_id(user.id)
    assert updated is not None
    assert updated.full_name == "Manager Updated"


def test_edit_user_view_model_does_not_save_without_changes() -> None:
    users = InMemoryUserRepository()
    user = _user("manager", "manager@sigesm.local", "Manager User")
    users.add(user)
    factory = InMemoryUserUpdateUnitOfWorkFactory(users)
    view_model = EditUserViewModel(_listing_item(users), EditUserService(factory))

    view_model.submit()

    assert factory.created == []


def test_edit_user_view_model_reports_validation_and_preserves_input() -> None:
    users = InMemoryUserRepository()
    user = _user("manager", "manager@sigesm.local", "Manager User")
    users.add(user)
    view_model = EditUserViewModel(
        _listing_item(users),
        EditUserService(InMemoryUserUpdateUnitOfWorkFactory(users)),
    )
    view_model.update_input("email", " ")

    view_model.submit()

    assert view_model.field_errors["email"] == "E-mail e obrigatorio."
    assert view_model.full_name == "Manager User"
    assert view_model.username == "manager"
    assert view_model.email == " "


def test_edit_user_view_model_blocks_double_submit_while_loading() -> None:
    users = InMemoryUserRepository()
    user = _user("manager", "manager@sigesm.local", "Manager User")
    users.add(user)
    view_model = EditUserViewModel(
        _listing_item(users),
        EditUserService(InMemoryUserUpdateUnitOfWorkFactory(users)),
    )
    view_model.update_input("full_name", "Manager Updated")
    view_model._set_loading(True)

    view_model.submit()

    assert view_model.is_loading


def test_user_form_dialog_edit_mode_has_no_password_fields_and_blocks_save(
    qt_app: QApplication,
) -> None:
    users = InMemoryUserRepository()
    users.add(_user("manager", "manager@sigesm.local", "Manager User"))
    view_model = EditUserViewModel(
        _listing_item(users),
        EditUserService(InMemoryUserUpdateUnitOfWorkFactory(users)),
    )
    dialog = UserFormDialog(view_model)

    assert dialog.windowTitle() == "Editar usuario"
    assert not dialog._password.isVisible()
    assert not dialog._password_confirmation.isVisible()
    assert dialog._full_name.text() == "Manager User"
    assert not dialog._save_button.isEnabled()

    view_model.update_input("full_name", "Manager Updated")
    dialog._sync_state()

    assert dialog._save_button.isEnabled()
    dialog.reject()
    qt_app.processEvents()


def test_sqlalchemy_user_update_persists_and_listing_reflects_change(
    identity_session_factory: DatabaseSessionFactory,
) -> None:
    with identity_session_factory.context() as session:
        repository = SqlAlchemyUserRepository(session)
        user = _user("manager", "manager@sigesm.local", "Manager User")
        repository.add(user)
        session.commit()
        user_id = str(user.id)

    update_service = EditUserService(
        SqlAlchemyUserUpdateUnitOfWorkFactory(identity_session_factory)
    )
    result = update_service.update_user(
        UpdateUserCommand(user_id, "Manager Updated", "manager2", "manager2@sigesm.local")
    )

    assert result.is_success
    with identity_session_factory.context() as session:
        repository = SqlAlchemyUserRepository(session)
        persisted = repository.get_by_id(Identity.from_string(user_id))
        assert persisted is not None
        assert persisted.full_name == "Manager Updated"
        assert persisted.username.value == "manager2"
        assert persisted.password_hash.value == _VALID_ARGON2ID_HASH


def test_sqlalchemy_user_update_duplicate_rolls_back(
    identity_session_factory: DatabaseSessionFactory,
) -> None:
    with identity_session_factory.context() as session:
        repository = SqlAlchemyUserRepository(session)
        user = _user("manager", "manager@sigesm.local", "Manager User")
        other = _user("other", "other@sigesm.local", "Other User")
        repository.add(user)
        repository.add(other)
        session.commit()
        user_id = str(user.id)

    update_service = EditUserService(
        SqlAlchemyUserUpdateUnitOfWorkFactory(identity_session_factory)
    )
    result = update_service.update_user(
        UpdateUserCommand(user_id, "Manager Updated", "other", "manager2@sigesm.local")
    )

    assert result.is_failure
    with identity_session_factory.context() as session:
        repository = SqlAlchemyUserRepository(session)
        persisted = repository.get_by_id(Identity.from_string(user_id))
        assert persisted is not None
        assert persisted.username.value == "manager"
        assert persisted.full_name == "Manager User"


def _user(username: str, email: str, full_name: str) -> User:
    return User.create(
        Username(username),
        Email(email),
        PasswordHash(_VALID_ARGON2ID_HASH),
        full_name=full_name,
    )


def _listing_item(users: InMemoryUserRepository) -> UserListItemDTO:
    result = UserListingService(InMemoryUserListingRepository(users)).list_users(ListUsersQuery())
    assert result.is_success
    return result.value.items[0]
