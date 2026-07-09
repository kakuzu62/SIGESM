# Relatorio de Implementacao - Release 1.1

## Objetivo

Implementar o nucleo de autenticacao do SIGESM Enterprise e iniciar o Desktop
Framework reutilizavel, sem criar telas de negocio.

## Authentication Core

Foram criados no dominio:

- `AuthenticationService`.
- `AuthenticationSession`.
- `RefreshSession`.
- `PasswordResetRequest`.
- `AuthenticationAttempt`.

O servico de senha foi migrado para Argon2id usando `argon2-cffi`. Tokens de
acesso, refresh e reset sao gerados como valores opacos e persistidos apenas
como SHA-256.

## Application

Foram adicionados use cases para:

- `AuthenticateUser`.
- `LogoutUser`.
- `RequestPasswordReset`.
- `ConfirmPasswordReset`.
- `ValidateSession`.
- `RenewSession`.

O use case de troca de senha existente permanece disponivel e o dominio tambem
expoe troca autenticada por `AuthenticationService.change_password`.

## Infraestrutura

Foram adicionados models e repositories SQLAlchemy para:

- sessoes de autenticacao;
- sessoes de refresh;
- solicitacoes de recuperacao de senha;
- tentativas de login.

## Segurança

- Hash de senha com Argon2id.
- Verificacao de senha delegada a biblioteca segura.
- Politica configuravel de bloqueio por tentativas.
- Auditoria inicial por `AuthenticationAttempt`.
- Expiracao configuravel de sessao, refresh e reset de senha.

## Desktop Framework

Foi criada a estrutura reutilizavel em `src/presentation/framework`:

- `shell`;
- `navigation`;
- `workspace`;
- `dialogs`;
- `components`;
- `themes`;
- `resources`;
- `commands`;
- `viewmodels`.

Nenhuma tela de negocio foi implementada.

## Validacoes

Validacoes executadas ao final da release:

- Black.
- Ruff.
- MyPy strict.
- PyTest.

## Observacoes

Nenhuma migration Alembic foi criada nesta release. Os models SQLAlchemy foram
preparados para uma etapa futura de migrations.
