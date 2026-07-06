# SIGESM Enterprise

Projeto corporativo em Python 3.12 com PySide6, SQLAlchemy 2 e Clean Architecture.

## Sprint 0.3 - Consolidacao Arquitetural

A base da Sprint 0 foi consolidada com auditoria entre camadas, MyPy strict,
Ruff, Black e testes automatizados. O dominio permanece desacoplado de
infraestrutura e interface, os contratos de persistencia nao dependem de
SQLAlchemy e a hierarquia de excecoes foi estabilizada para uso corporativo.

As decisoes arquitetonicas estao registradas em `docs/DECISIONS.md`.

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

O contrato `IUnitOfWork` do dominio usa tipos neutros de infraestrutura. A
implementacao SQLAlchemy fica isolada em `infrastructure`, preservando Clean
Architecture e facilitando a troca futura do mecanismo de persistencia.

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

## Escalas de Servico

O contexto `src/domain/service_scale` modela escalas PRETA e VERMELHA, funcoes
de servico, designacoes de militares e politicas de descanso. As regras iniciais
consideram servicos de 24 horas, descanso minimo padrao de 78 horas e excecao
controlada para escala 1x1.

O pacote tambem inclui um motor de elegibilidade desacoplado da infraestrutura.
Ele avalia militares por pipeline de specifications, retornando todos os motivos
de inelegibilidade e emitindo eventos de dominio para decisoes elegiveis ou
inelegiveis.

O `ScaleGenerationEngine` gera automaticamente escalas a partir de strategies por
tipo de escala, policy de geracao, fairness, calculo de descanso e motor de
elegibilidade. Ele retorna estatisticas, descartes, selecionados e eventos de
dominio sem depender de interface ou infraestrutura.

## Trocas e Vendas de Servico

O contexto `src/domain/service_exchange` modela troca oficial e venda de
servico. A troca oficial valida os dois militares nos novos dias assumidos. A
venda registra servico extraordinario do comprador, preserva o contador base do
comprador e zera normalmente o vendedor, com decisoes auditaveis.
