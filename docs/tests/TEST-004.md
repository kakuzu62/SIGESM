# TEST-004 - Plano de Testes da STS-001D

## Domain

- ativacao valida;
- desativacao valida;
- `updated_at` atualizado em mudanca real;
- mesmo estado tratado como idempotente no dominio;
- ID, senha, dados cadastrais, roles e `created_at` preservados.

## Application

- ativacao com sucesso;
- desativacao com sucesso;
- usuario inexistente;
- auto-desativacao rejeitada;
- autoativacao permitida;
- mesmo estado rejeitado com mensagem compreensivel;
- commit no sucesso;
- rollback na falha;
- conflito tecnico traduzido;
- DTO sem senha/hash.

## Presentation

- selecao vazia nao chama Application;
- confirmacao emitida;
- cancelamento nao chama Application;
- sucesso emitido;
- falha emitida;
- `actor_user_id` usado no Command.

## Integration

- status persistido no SQLite;
- rollback preserva estado anterior;
- listagem reflete mudanca;
- autenticacao rejeita usuario inativo.

## Quality Gate Local

- Black: aprovado, 471 arquivos verificados.
- Ruff: aprovado, sem violacoes.
- MyPy strict: aprovado, 471 arquivos analisados.
- PyTest: aprovado, 156 testes executados.
