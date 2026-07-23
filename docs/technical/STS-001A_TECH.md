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

### ViewModel

`UserListViewModel` representa apenas estado e intencoes da tela. A ViewModel
expoe:

- `users`
- `page`
- `total`
- `total_pages`
- `error_message`
- `is_loading`

Apos carregamento bem-sucedido, a ViewModel notifica todas as propriedades
afetadas pela consulta. Em caso de falha, preserva a pagina anterior e atualiza
`error_message`.

### Eventos de Interface

Abertura de dialogos e tratada por sinais explicitos:

- `new_user_requested`
- `edit_user_requested`

Esses sinais substituem propriedades transitorias e evitam representar eventos
como estado persistente. A View apenas conecta os sinais aos dialogos, sem
executar regra de negocio.

### Preparacao para Persistencia Real

`is_loading` e ativado durante `load()` e restaurado em bloco `finally`. A View
usa esse estado para bloquear controles incompativeis durante a consulta. A
execucao continua sincronona nesta STS; concorrencia sera introduzida em uma
etapa posterior, com mecanismo centralizado.

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

## Debito Arquitetural

O slice esta temporariamente localizado em
`src/presentation/modules/user_management/`. A estrutura interna segue Vertical
Slice, mas a localizacao fisica deve ser movida para um namespace neutro antes
do crescimento do modulo.
