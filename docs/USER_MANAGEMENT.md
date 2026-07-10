# User Management

## STS-001A - Listagem de Usuarios

A listagem de usuarios e a primeira funcionalidade visivel do Epico
Administracao.

## Fluxo

```text
UserListView
  -> UserListViewModel
  -> UserListingService
  -> ListUsersHandler / SearchUsersHandler
  -> IUserListingRepository
  -> Infrastructure
```

## MVVM

- A View monta a tela, tabela, pesquisa, toolbar e paginacao.
- O ViewModel controla carregamento, pesquisa, pagina, ordenacao e abertura dos
  dialogos.
- A View nao acessa repositories, SQLAlchemy ou objetos de persistencia.

## Pesquisa

A pesquisa usa `filter_text` em `ListUsersQuery`. O widget ja reage a alteracao
incremental de texto e permanece preparado para debounce futuro.

## Paginacao

`PagedResult[T]` retorna:

- items;
- total;
- page;
- page_size;
- total_pages.

A tela carrega apenas a pagina atual.

## Ordenacao

`UserTableModel` traduz colunas para campos de ordenacao. O ViewModel alterna
direcao ASC/DESC quando a mesma coluna e selecionada novamente.

## Dialogos

`UserFormDialog` abre para novo usuario e edicao, mas nao persiste alteracoes
nesta STS. Criacao e edicao serao entregues nas proximas STSs.
