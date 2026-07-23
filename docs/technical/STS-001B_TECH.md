# STS-001B TECH - Cadastro de Usuarios

## Application

Criado o slice:

```text
src/presentation/modules/user_management/application/commands/create_user/
```

Componentes:

- `CreateUserCommand`;
- `CreateUserCommandValidator`;
- `CreateUserHandler`;
- `CreateUserResultDTO`;
- `UserCreationUnitOfWork`;
- `UserCreationUnitOfWorkFactory`;
- `CreateUserService`.

O `password_confirmation` permanece na Presentation e nao entra no Command.

## Domain

O agregado `domain.identity.entities.User` foi reutilizado. O dominio passou a
armazenar `full_name`, com normalizacao de espacos e limite maximo de 120
caracteres. Chamadas antigas continuam compativeis usando o username como
fallback.

## Infrastructure

Criado adapter em memoria:

- `InMemoryUserCreationUnitOfWork`;
- `InMemoryUserCreationUnitOfWorkFactory`.

Criado adapter SQLAlchemy:

- `SqlAlchemyUserCreationUnitOfWork`;
- `SqlAlchemyUserCreationUnitOfWorkFactory`.

O adapter SQLAlchemy reutiliza `SqlAlchemyUserRepository` do Identity Context e
traduz `IntegrityError` em `UserCreationConflictError`, impedindo vazamento de
detalhes internos para a interface.

## Persistence

`identity_users` recebeu a coluna obrigatoria `full_name`.

Migration:

```text
migrations/versions/20260723_0001_add_identity_user_full_name.py
```

A migration preenche usuarios existentes com o valor de `username` antes de
tornar a coluna obrigatoria.

## Presentation

Criados:

- `CreateUserViewModel`;
- `CreateUserInput`;
- formulario real em `UserFormDialog`.

A ViewModel expoe `is_loading`, `can_submit`, `field_errors` e `general_error`.
Sinais:

- `user_created`;
- `creation_failed`.

O dialogo nao acessa repository, SQLAlchemy, session, engine ou Unit of Work.

## Seguranca

- senha nunca e retornada em DTO;
- hash nao e exposto na listagem nem no resultado da criacao;
- View nao executa hashing;
- senha nao e enviada em sinais;
- erros tecnicos de unicidade sao traduzidos para mensagens de aplicacao.

## Debitos

AR-001-01 permanece aberto: o slice `user_management` ainda esta sob
`src/presentation/modules/` e deve ser realocado em refatoracao controlada.

