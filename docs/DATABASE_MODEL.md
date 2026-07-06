# Database Model

Diretrizes para modelo de dados e persistencia.

## Estrategia

- SQLite e o banco local inicial.
- O desenho deve permanecer compativel com PostgreSQL.
- SQLAlchemy 2 e Alembic sao as ferramentas oficiais de ORM e migrations.

## Convencoes de Nome

- Tabelas em snake_case e plural apenas quando o contexto exigir consistencia.
- Colunas em snake_case.
- Indices com prefixo `ix_`.
- Unique constraints com prefixo `uq_`.
- Foreign keys com prefixo `fk_`.
- Check constraints com prefixo `ck_`.

## Chaves

- Chaves primarias devem ser estaveis e explicitas.
- Chaves estrangeiras devem preservar integridade referencial.
- Identificadores de dominio podem usar UUID quando fizer sentido.

## Migrations Alembic

- Toda alteracao estrutural deve gerar migration.
- Migration deve ter nome claro e reversao quando viavel.
- Migrations nao devem carregar regra de negocio.

## Indices

- Criar indices para filtros frequentes, relatorios e integridade.
- Evitar indices antes de existir necessidade operacional clara.

## Auditoria e Timestamps

- Entidades persistidas devem possuir `created_at` e `updated_at` quando
  aplicavel.
- Registros auditaveis devem guardar ator, origem, acao e metadata.

## Soft Delete

- Usar soft delete quando houver requisito de historico ou auditoria.
- Exclusao fisica deve ser restrita a dados temporarios ou tecnicos.
