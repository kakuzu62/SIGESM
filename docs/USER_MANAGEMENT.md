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

`UserFormDialog` abre o formulario real de novo usuario quando recebe
`CreateUserViewModel`. O modo de edicao permanece somente leitura nesta STS.

## STS-001B - Cadastro de Usuarios

Fluxo:

```text
UserFormDialog
  -> CreateUserViewModel
  -> CreateUserService
  -> CreateUserCommand
  -> CreateUserHandler
  -> IUserRepository
  -> UserCreationUnitOfWork
```

Campos:

- nome completo;
- login;
- e-mail;
- senha inicial;
- confirmacao da senha.

A confirmacao da senha existe apenas na Presentation e nao e enviada para
Application, Domain ou Persistence.

## Politica de Sucesso e Falha

- Sucesso fecha o dialogo, limpa senhas e atualiza a consulta atual da listagem.
- Falha mantem o dialogo aberto e preserva dados nao sensiveis.
- Login e e-mail duplicados sao exibidos como mensagens compreensiveis.
- Senha e hash nao sao retornados em DTO, sinais ou mensagens.
