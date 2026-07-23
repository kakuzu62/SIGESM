# STS-001C - Edicao de Usuarios

## Status

Implementada para revisao AR-003.

## Objetivo

Permitir que um administrador edite dados cadastrais de um usuario existente,
mantendo Clean Architecture, CQRS, MVVM, Repository Pattern, Unit of Work e
Result Pattern.

## Escopo

Incluido:

- edicao de nome completo;
- edicao de login;
- edicao de e-mail;
- validacoes por campo;
- protecao contra duplicidade;
- preservacao de senha, status, roles e timestamps imutaveis;
- atualizacao da listagem apos sucesso.

Fora de escopo:

- redefinicao de senha;
- ativacao e desativacao;
- perfis;
- permissoes;
- auditoria;
- exclusao.

## Fluxo Funcional

```text
UserListView
  -> UserFormDialog
  -> EditUserViewModel
  -> EditUserService
  -> UpdateUserCommand
  -> UpdateUserHandler
  -> IUserRepository
  -> UserUpdateUnitOfWork
  -> Persistence
```

## Politica de Listagem Apos Edicao

A consulta atual e atualizada apos sucesso sem alterar filtro, ordenacao ou
pagina. Caso o registro editado deixe de corresponder ao filtro atual, a tela
mantem o filtro e exibe a mensagem de sucesso.

