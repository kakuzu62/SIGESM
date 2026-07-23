# STS-001C TECH - Edicao de Usuarios

## Application

Criado o slice:

```text
src/presentation/modules/user_management/application/commands/update_user/
```

Componentes:

- `UpdateUserCommand`;
- `UpdateUserCommandValidator`;
- `UpdateUserHandler`;
- `UpdateUserResultDTO`;
- `UserUpdateUnitOfWork`;
- `UserUpdateUnitOfWorkFactory`;
- `EditUserService`.

O Command contem somente `user_id`, `full_name`, `username` e `email`.

## Domain

O agregado `User` recebeu `update_profile()`. O metodo altera apenas nome
completo, login, e-mail e `updated_at`. Permanecem preservados:

- id;
- password_hash;
- active;
- roles;
- created_at.

## Infrastructure

Criado adapter em memoria:

- `InMemoryUserUpdateUnitOfWork`;
- `InMemoryUserUpdateUnitOfWorkFactory`.

Criado adapter SQLAlchemy:

- `SqlAlchemyUserUpdateUnitOfWork`;
- `SqlAlchemyUserUpdateUnitOfWorkFactory`.

O adapter SQLAlchemy reutiliza `SqlAlchemyUserRepository` do Identity Context e
traduz `IntegrityError` em `UserUpdateConflictError`.

## Presentation

Criados:

- `EditUserViewModel`;
- `EditUserInput`;
- modo edicao real em `UserFormDialog`.

A ViewModel expoe `user_id`, `full_name`, `username`, `email`, `is_loading`,
`can_submit`, `field_errors`, `general_error` e `has_changes`.

Sinais:

- `user_updated`;
- `update_failed`.

O dialogo de edicao nao exibe campos de senha.

## Concorrencia

O modelo `User` ainda nao possui `version_id` ou controle otimista. A STS-001C
mantem a semantica atual de last-write-wins e registra a necessidade de uma STS
futura para versionamento otimista, migration e testes especificos.

## Debitos

- AR-001-01 permanece aberto: realocar `user_management` para fora de
  `src/presentation/modules/`.
- Execucao de UI ainda e sincronona; uma infraestrutura de background tasks deve
  ser criada antes de consultas ou escritas pesadas.

