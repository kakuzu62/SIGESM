# Database Model

Este documento complementa `DATA_ARCHITECTURE.md` com convencoes oficiais para
o modelo fisico do banco do SIGESM Enterprise. A Release 0.5 nao cria tabelas nem
migrations.

## Estrategia

- SQLite e o banco local inicial.
- PostgreSQL e o alvo de compatibilidade corporativa futura.
- SQLAlchemy 2 e Alembic sao as ferramentas oficiais de ORM e migrations.
- O dominio nao deve depender do formato fisico do banco.

## Convencoes de Tabelas

- Tabelas em `snake_case`.
- Nome deve representar o conceito persistido, nao a tela.
- Tabelas por bounded context devem usar nomes claros, por exemplo
  `military_persons`, `service_assignments` e `audit_entries`.
- Tabelas associativas usam nomes compostos: `user_profiles`,
  `profile_permissions`.

## Convencoes de Colunas

- Colunas em `snake_case`.
- Chave primaria: `id`.
- Foreign keys: `<referenced_table_singular>_id` quando a leitura permanecer
  clara.
- Timestamps padrao: `created_at`, `updated_at`, `deleted_at`.
- Responsaveis por alteracao: `created_by`, `updated_by`, `deleted_by` quando
  houver auditoria de usuario.
- Status devem ser armazenados como strings estaveis, nao como inteiros magicos.

## Constraints e Indices

- Primary key: `pk_<table>`.
- Foreign key: `fk_<table>__<column>__<referenced_table>`.
- Unique constraint: `uq_<table>__<columns>`.
- Check constraint: `ck_<table>__<rule>`.
- Index: `ix_<table>__<columns>`.
- Indices devem priorizar consultas por periodo, status, militar, escala e
  organizacao.

## Tipos Portaveis

- UUID: texto canonico inicialmente.
- CPF, telefone e codigos: strings normalizadas.
- Datas: tipos de data ou datetime do SQLAlchemy.
- Metadata: JSON apenas quando a estrutura for flexivel por natureza.
- Valores monetarios futuros: decimal, nunca float.

## Auditoria

- Toda acao sensivel deve gerar `audit_entries`.
- Decisoes automaticas devem gerar `decision_records`.
- Eventos de dominio podem ser persistidos em `domain_event_outbox` quando o
  projeto adotar publicacao assíncrona.

## Timestamps

- `created_at` obrigatorio em registros operacionais.
- `updated_at` obrigatorio quando o registro puder mudar.
- Usar UTC como referencia tecnica e formatacao local na interface.

## Soft Delete

- Preferir `deleted_at` e `deleted_by` para registros auditaveis.
- Consultas padrao devem ignorar registros removidos logicamente.
- Relatorios de auditoria podem incluir registros removidos.

## Historico

- Historico especifico deve existir quando a transicao tiver significado de
  negocio, como mudanca de posto, contato, escala ou parametro.
- Auditoria registra o fato; tabela historica registra o estado relevante para
  consulta operacional.

## Alembic

- Migrations devem usar naming convention centralizada.
- Revisoes devem ser pequenas e ordenadas.
- Downgrade deve ser implementado quando seguro.
- Seeds operacionais devem ficar separados de schema.

## Identity - Modelo Fisico Inicial

A Release 1.0 prepara os models SQLAlchemy do contexto Identity. A STS-001B
adiciona a primeira migration versionada para suportar cadastro de usuarios com
nome completo. As tabelas planejadas para o contexto sao:

- `identity_users`: usuarios, nome completo, username, email, hash de senha,
  status ativo, tentativas falhas, bloqueio e timestamps.
- `identity_roles`: perfis de acesso.
- `identity_permissions`: permissoes atomicas.
- `identity_user_roles`: associacao muitos-para-muitos entre usuarios e roles.
- `identity_role_permissions`: associacao muitos-para-muitos entre roles e
  permissoes.
- `identity_user_sessions`: sessoes de usuario e status de sessao.
- `identity_authentication_sessions`: sessoes de autenticacao com hash do token
  de acesso.
- `identity_refresh_sessions`: refresh tokens persistidos por hash.
- `identity_password_reset_requests`: recuperacao de senha com hash do token de
  reset e controle de uso.
- `identity_authentication_attempts`: auditoria de tentativas de login.

Senhas nunca devem ser armazenadas em texto puro. O campo `password_hash` deve
conter apenas o hash Argon2id codificado produzido pelo servico de senha do
dominio. Tokens de acesso, refresh e reset tambem nao devem ser persistidos em
texto puro.

### STS-001B

Migration:

```text
migrations/versions/20260723_0001_add_identity_user_full_name.py
```

A coluna `identity_users.full_name` e obrigatoria, possui limite de 120
caracteres e e preenchida com `username` para usuarios existentes durante a
migration.
