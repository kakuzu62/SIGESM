# STS-001D TECH - Ativacao e Desativacao de Usuarios

## Fluxo

```text
UserListView
  -> ChangeUserActiveStatusViewModel
  -> ChangeUserActiveStatusService
  -> ChangeUserActiveStatusCommand
  -> ChangeUserActiveStatusHandler
  -> IUserRepository
  -> UserStatusUnitOfWork
  -> Persistence
```

## Application

A fatia CQRS adiciona:

- `ChangeUserActiveStatusCommand`;
- `ChangeUserActiveStatusCommandValidator`;
- `ChangeUserActiveStatusHandler`;
- `ChangeUserActiveStatusResultDTO`;
- `ChangeUserActiveStatusService`;
- `UserStatusUnitOfWork`.

O comando transporta apenas `actor_user_id`, `target_user_id` e `is_active`.

## Domain

O agregado `User` continua sendo o unico modelo de usuario. Os metodos
`activate()` e `deactivate()` preservam os dados cadastrais, credenciais,
roles, permissoes e `created_at`.

## Presentation

`ChangeUserActiveStatusViewModel` controla selecao, confirmacao, loading e
resultado. A View exibe apenas a confirmacao e encaminha a decisao do usuario
para a ViewModel.

## Persistencia

Foram criadas Unit of Work em memoria e SQLAlchemy. Nao houve alteracao de
schema e nenhuma migration foi necessaria.

## Debitos

- AR-001-01: realocar `user_management` para fora de `src/presentation/modules/`.
- Controle otimista ausente: comportamento atual e last-write-wins.
- Execucao da UI ainda sincronona.
- Protecao do ultimo administrador depende de roles/permissoes formais.
