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

## STS-001C - Edicao de Usuarios

Fluxo:

```text
UserListView
  -> UserFormDialog
  -> EditUserViewModel
  -> EditUserService
  -> UpdateUserCommand
  -> UpdateUserHandler
  -> IUserRepository
  -> UserUpdateUnitOfWork
```

Campos editaveis:

- nome completo;
- login;
- e-mail.

O modo edicao nao exibe senha, confirmacao, hash, tokens ou detalhes internos de
autenticacao.

## Politica de Edicao

- Salvar permanece desabilitado quando nao houver alteracoes.
- O proprio login/e-mail atual do usuario nao e tratado como duplicidade.
- Login/e-mail pertencentes a outro usuario sao rejeitados.
- Senha, estado ativo, roles e `created_at` sao preservados.
- A listagem e atualizada apos sucesso mantendo filtro, ordenacao e pagina.
- Controle otimista ainda nao existe; o comportamento atual e last-write-wins.

## STS-001D - Ativacao e Desativacao de Usuarios

Fluxo:

```text
UserListView
  -> ChangeUserActiveStatusViewModel
  -> ChangeUserActiveStatusService
  -> ChangeUserActiveStatusCommand
  -> ChangeUserActiveStatusHandler
  -> IUserRepository
  -> UserStatusUnitOfWork
```

## Politica de Status

- A toolbar exibe ativar para usuarios inativos e desativar para usuarios
  ativos.
- Toda mudanca exige confirmacao explicita.
- Cancelar a confirmacao nao chama a camada Application.
- O ator autenticado e enviado no Command como `actor_user_id`.
- A auto-desativacao e bloqueada no Application Handler, nao apenas na UI.
- Usuario inativo e rejeitado pelo Authentication Core.
- A listagem e atualizada apos sucesso mantendo filtro, ordenacao e pagina.
- A protecao do ultimo administrador sera implementada quando roles/permissoes
  estiverem formalmente disponiveis no modulo administrativo.

## STS-001E - Redefinicao de Senha

Fluxo:

```text
UserListView
  -> ResetPasswordDialog
  -> ResetPasswordViewModel
  -> ResetPasswordService
  -> ResetPasswordCommand
  -> ResetPasswordHandler
  -> PasswordService
  -> IUserRepository
  -> ResetPasswordUnitOfWork
```

## Politica de Redefinicao

- O dialogo possui apenas nova senha e confirmacao.
- A confirmacao permanece restrita a Presentation.
- A politica de senha e aplicada exclusivamente pelo `PasswordService`.
- Senha e hash nao trafegam em DTOs, sinais, logs ou mensagens.
- Sucesso limpa campos sensiveis, fecha o dialogo e atualiza a listagem.
- Cancelamento limpa os campos e nao chama Application.
- Invalidacao de sessoes ativas fica pendente ate definicao formal de politica.
