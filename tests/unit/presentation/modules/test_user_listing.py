from __future__ import annotations

from domain.identity.entities import User
from domain.identity.services import PasswordService
from domain.identity.value_objects import Email, Username
from infrastructure.identity import InMemoryUserRepository
from presentation.modules.user_management.application import UserListingService
from presentation.modules.user_management.application.common import SortDirection
from presentation.modules.user_management.application.queries.list_users import (
    ListUsersHandler,
    ListUsersQuery,
)
from presentation.modules.user_management.infrastructure.repositories import (
    InMemoryUserListingRepository,
)
from presentation.modules.user_management.presentation.models import UserTableModel
from presentation.modules.user_management.presentation.viewmodels import UserListViewModel


def test_list_users_handler_returns_paged_users() -> None:
    repository = _repository_with_users("admin", "operator")
    handler = ListUsersHandler(repository)

    result = handler.handle(ListUsersQuery(page=1, page_size=1))

    assert result.is_success
    assert result.value.total == 2
    assert len(result.value.items) == 1


def test_list_users_handler_searches_users() -> None:
    repository = _repository_with_users("admin", "operator")
    handler = ListUsersHandler(repository)

    result = handler.handle(ListUsersQuery(filter_text="oper"))

    assert result.is_success
    assert tuple(item.login for item in result.value.items) == ("operator",)


def test_list_users_handler_orders_descending() -> None:
    repository = _repository_with_users("admin", "operator")
    handler = ListUsersHandler(repository)

    result = handler.handle(ListUsersQuery(sort_by="login", direction=SortDirection.DESC))

    assert result.is_success
    assert tuple(item.login for item in result.value.items) == ("operator", "admin")


def test_user_list_view_model_loads_and_changes_page() -> None:
    view_model = UserListViewModel(
        UserListingService(_repository_with_users("alpha", "bravo", "charlie"))
    )

    view_model.load()
    view_model.change_page(1)

    assert view_model.total == 3
    assert view_model.page == 1


def test_user_list_view_model_searches() -> None:
    view_model = UserListViewModel(UserListingService(_repository_with_users("admin", "operator")))

    view_model.search("admin")

    assert tuple(item.login for item in view_model.users) == ("admin",)


def test_user_table_model_displays_user_data() -> None:
    result = _repository_with_users("admin").list_users(ListUsersQuery())
    model = UserTableModel()

    model.set_items(result.items)

    assert model.rowCount() == 1
    assert model.columnCount() == 6
    assert model.data(model.index(0, 0)) == "admin"


def _repository_with_users(*usernames: str) -> InMemoryUserListingRepository:
    users = InMemoryUserRepository()
    password_service = PasswordService()
    for username in usernames:
        users.add(
            User.create(
                Username(username),
                Email(f"{username}@sigesm.local"),
                password_service.hash_password("Strong#123"),
            )
        )
    return InMemoryUserListingRepository(users)
