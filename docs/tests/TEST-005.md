# TEST-005 - Plano de Testes da STS-001E

## Domain

- `change_password` altera hash;
- `updated_at` e atualizado;
- ID, dados cadastrais, estado, roles e `created_at` sao preservados.

## Application

- senha vazia rejeitada;
- identificadores invalidos rejeitados;
- usuario inexistente;
- sucesso;
- commit no sucesso;
- rollback na falha;
- `PasswordService` chamado;
- DTO sem senha/hash;
- politica de senha aplicada.

## Presentation

- campos obrigatorios;
- confirmacao divergente;
- `is_loading`;
- `can_submit`;
- campos limpos apos sucesso;
- dialogo cancela sem persistir;
- campos mascarados.

## Integration

- SQLite persiste novo hash;
- senha antiga rejeitada;
- senha nova aceita;
- regressao completa preservada.

## Quality Gate Local

- Black: aprovado, 483 arquivos verificados.
- Ruff: aprovado, sem violacoes.
- MyPy strict: aprovado, 483 arquivos analisados.
- PyTest: aprovado, 167 testes executados.
