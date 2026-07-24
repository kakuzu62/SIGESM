# STS-001E TECH - Redefinicao de Senha

## Fluxo

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
  -> Persistence
```

## Application

A fatia CQRS adiciona:

- `ResetPasswordCommand`;
- `ResetPasswordCommandValidator`;
- `ResetPasswordHandler`;
- `ResetPasswordResultDTO`;
- `ResetPasswordService`;
- `ResetPasswordUnitOfWork`.

O comando transporta `actor_user_id`, `target_user_id` e `new_password`. A
confirmacao de senha existe apenas na Presentation.

## Domain

O agregado `User` recebeu `change_password(password_hash, occurred_at=None)`.
O hash e gerado exclusivamente pelo `PasswordService`.

## Presentation

`ResetPasswordDialog` e separado de `UserFormDialog`. Ele possui apenas nova
senha e confirmacao, ambos mascarados. `ResetPasswordViewModel` limpa os campos
apos sucesso e cancelamento.

## Persistencia

Foram criadas Unit of Work em memoria e SQLAlchemy. Nenhuma migration foi
necessaria.

## Seguranca

DTOs e sinais nao incluem senha ou hash. Logs tecnicos nao recebem senha. A
invalidacao de sessoes ativas fica registrada como debito ate haver politica
formal para esse comportamento.
