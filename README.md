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

## Dominio Militar

O contexto militar inicial esta em `src/domain/military`. Ele modela o agregado
`MilitaryPerson`, value objects para identificacao militar, CPF, telefone,
nome completo, posto/graduacao e status operacional, alem do evento de dominio
`MilitaryRegistered`.

## Organizacao Militar

O contexto `src/domain/organization` modela organizacoes militares como bounded
context separado. Ele contem o agregado `Organization`, value objects de codigo,
nome, abreviatura e localizacao, evento `OrganizationCreated`, contrato de
repositorio e specification para verificar duplicidade de codigo.
