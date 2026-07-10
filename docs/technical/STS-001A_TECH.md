# STS-001A TECH - Listagem de Usuarios

## Arquitetura

Fluxo obrigatorio:

```text
UserListView
  -> UserListViewModel
  -> UserListingService
  -> ListUsersHandler / SearchUsersHandler
  -> IUserListingRepository
  -> Infrastructure
```

## Vertical Slice

Modulo:

```text
src/presentation/modules/user_management/
```

Subcamadas:

- `application`
- `domain`
- `infrastructure`
- `presentation`

## Application

Criado:

- `ListUsersQuery`
- `ListUsersHandler`
- `ListUsersValidator`
- `UserListItemDTO`
- `SearchUsersQuery`
- `SearchUsersHandler`
- `UserListingService`
- `PagedResult`
- `SortDirection`

## Domain

Criado:

- `IUserListingRepository`

Contrato exposto:

- `list_users`
- `search`
- `order`
- `paginate`
- `total`

## Infrastructure

Criado:

- `InMemoryUserListingRepository`
- `SqlAlchemyUserListingRepository`

O adapter em memoria atende desktop local e testes. O adapter SQLAlchemy fica
preparado para a persistencia real sem ser acessado pela Presentation.

## Presentation

Criado:

- `UserListView`
- `UserListViewModel`
- `UserTableModel`
- `SearchBar`
- `PaginationWidget`
- `UserFormDialog`

O shell registra o modulo `Usuarios` por meio de `NavigationService`.

## Dependencias Permitidas

- Presentation -> Application
- Application -> Domain
- Infrastructure -> Domain/Application contracts
- Domain sem dependencia de UI ou SQLAlchemy

## Dependencias Proibidas

- View -> SQLAlchemy
- View -> Repository
- View -> Domain rules
- ViewModel -> SQLAlchemy
- QMainWindow -> regra de negocio
