# SIGESM Enterprise

Projeto corporativo em Python 3.12 com PySide6, SQLAlchemy 2 e Clean Architecture.

## Kernel compartilhado

O projeto possui um Shared Kernel em `src/shared/kernel` com as bases para DDD:
entidades, aggregate roots, value objects, identidades UUID, eventos de dominio,
result pattern, notification pattern, guard clauses, specifications e despacho
sincrono de eventos. O pacote tambem inclui um container simples de injecao de
dependencias em `src/bootstrap/container.py`.

## Persistencia

A infraestrutura de persistencia combina contratos de dominio em `src/domain`
com adapters SQLAlchemy em `src/infrastructure/persistence/sqlalchemy`. A camada
oferece repository base, session context, transaction manager com savepoints e
Unit of Work transacional, usando as configuracoes centralizadas em
`core.config.settings`.
