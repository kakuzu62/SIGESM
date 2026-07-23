# STS-001B - Cadastro de Usuarios

## Status

Implementada para revisao AR-002.

## Objetivo

Transformar o formulario placeholder de novo usuario em um fluxo real de
criacao, mantendo Clean Architecture, CQRS, MVVM, Repository Pattern, Unit of
Work e Result Pattern.

## Escopo

Incluido:

- formulario real de novo usuario;
- nome completo, login, e-mail, senha inicial e confirmacao de senha;
- validacoes por campo;
- criacao por Command e Handler;
- persistencia por repository e Unit of Work;
- protecao contra login e e-mail duplicados;
- feedback de sucesso e falha;
- atualizacao da listagem apos sucesso.

Fora de escopo:

- edicao;
- ativacao e desativacao;
- redefinicao de senha;
- perfis;
- permissoes;
- auditoria.

## Fluxo Funcional

```text
UserFormDialog
  -> CreateUserViewModel
  -> CreateUserService
  -> CreateUserCommand
  -> CreateUserHandler
  -> IUserRepository
  -> UserCreationUnitOfWork
  -> Persistence
```

## Politica de Listagem Apos Criacao

Apos sucesso, a consulta atual e atualizada sem alterar filtro, ordenacao ou
pagina silenciosamente. A mensagem de sucesso e exibida mesmo quando o novo
usuario nao aparece por causa do filtro atual.

