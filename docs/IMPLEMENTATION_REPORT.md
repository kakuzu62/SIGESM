# Relatorio de Implementacao - STS-001A

## Identificacao

- Epico: Administracao.
- Release: 2.1 - User Management.
- STS: 001A - Listagem de Usuarios.
- Branch: `codex/sts-001a-user-listing`.

## Objetivo

Entregar a primeira funcionalidade completa visivel ao usuario autenticado:
listagem de usuarios com pesquisa, ordenacao, paginacao e atualizacao.

## Entregas

- Modulo `Usuarios` integrado ao menu lateral.
- Query `ListUsersQuery`.
- Handler `ListUsersHandler`.
- Validator `ListUsersValidator`.
- DTO `UserListItemDTO` sem `PasswordHash`.
- Query de pesquisa `SearchUsersQuery`.
- Contrato `IUserListingRepository`.
- Adapter em memoria para desktop local e testes.
- Adapter SQLAlchemy de leitura com paginacao.
- `UserListViewModel`.
- `UserTableModel` baseado em `QAbstractTableModel`.
- `SearchBar`, `PaginationWidget` e `CrudToolbar`.
- `UserFormDialog` placeholder para novo/edicao.

## Arquitetura

A Presentation nao acessa banco nem repository diretamente. O fluxo e:

```text
UserListView -> UserListViewModel -> UserListingService -> Handlers -> Repository
```

## Validacoes

- Black: aprovado.
- Ruff: aprovado.
- MyPy strict: aprovado.
- PyTest: aprovado.

## AR-001R1

Correcoes aplicadas apos a Architecture Review AR-001:

- `UserListViewModel` passou a notificar `users`, `page`, `total`,
  `total_pages` e `error_message` apos consultas bem-sucedidas.
- Falhas preservam os dados anteriores e atualizam explicitamente
  `error_message`.
- Abertura de formulario de novo usuario e edicao passou a usar sinais
  explicitos.
- Adicionado `is_loading` para bloquear acoes duplicadas durante carregamento.
- Testes ampliados para validacoes, limites, falhas, sinais, estado de
  carregamento, tabela vazia e ausencia de dados sensiveis no DTO.

### Quality Gate AR-001R1

- Black: aprovado, 433 arquivos verificados.
- Ruff: aprovado, sem violacoes.
- MyPy strict: aprovado, 433 arquivos analisados.
- PyTest: aprovado, 112 testes executados.

## Observacoes

Nenhuma operacao de alteracao foi implementada nesta STS. Cadastro, edicao,
ativacao/desativacao, redefinicao de senha e associacao de perfis permanecem
planejadas para STS futuras.
