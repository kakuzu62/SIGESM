# TEST-006 - Plano de Testes da STS-001F

## Domain

- atribuicao valida;
- remocao valida;
- multiplos perfis;
- duplicidade impedida;
- mesma composicao idempotente;
- invariantes preservadas.

## Application

- usuario inexistente;
- perfil inexistente;
- perfil inativo;
- atribuicao com sucesso;
- remocao com sucesso;
- substituicao da composicao;
- protecao do ultimo Administrador ativo;
- autoalteracao segura;
- rollback em falha;
- DTO seguro.

## Query

- lista apenas perfis ativos;
- ordenacao estavel;
- DTO seguro.

## Presentation

- carregamento inicial;
- perfis atuais marcados;
- `has_changes`;
- `can_submit`;
- cancelamento sem persistir;
- sucesso fecha;
- falha preserva selecao.

## Persistence

- baseline Alembic cria o schema Identity em banco vazio;
- campos `normalized_name` e `active`;
- associacao persistida;
- remocao persistida;
- SQLite.

## Quality Gate Local

- Black: aprovado, 502 arquivos verificados.
- Ruff: aprovado.
- MyPy strict: aprovado, 502 arquivos verificados.
- PyTest: aprovado, 179 testes executados.
- Alembic `upgrade head` em banco vazio: aprovado.
- Alembic downgrade da revision `20260723_0002`: aprovado.
- Alembic upgrade da revision `20260723_0002`: aprovado.
