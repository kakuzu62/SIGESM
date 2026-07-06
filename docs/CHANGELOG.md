# Changelog

## Sprint 0.2A - Pacote 10

- Criado `ScaleGenerationEngine` para geracao automatica de escalas.
- Adicionados contextos, resultados e estatisticas de geracao.
- Criados services de selecao de candidatos, fairness e calculo de descanso.
- Criadas policies e strategies PRETA/VERMELHA.
- Adicionados eventos `ScaleGenerated`, `MilitarySelected` e `MilitarySkipped`.
- Criados testes unitarios do motor de geracao.

## Sprint 0.2A - Pacote 09

- Criado o motor de elegibilidade reutilizavel de escalas de servico.
- Adicionado pipeline de specifications para descanso, status, compatibilidade, conflitos e bloqueios.
- Criados `EligibilityResult` e `EligibilityReason`.
- Adicionada `EligibilityPolicy` configuravel.
- Criados eventos `MilitaryDeclaredEligible` e `MilitaryDeclaredIneligible`.
- Criados testes unitarios do motor de decisao.

## Sprint 0.2A - Pacote 08

- Criado o bounded context `domain.service_scale`.
- Adicionados agregados e entidades para escala, funcao de servico e designacao.
- Criadas regras de descanso minimo de 78 horas e excecao controlada 1x1.
- Adicionadas specifications de descanso e disponibilidade militar.
- Criado desempate deterministico preparado para auditoria.
- Criados eventos `ServiceAssignmentCreated` e `ServiceAssignmentCancelled`.

## Sprint 0.2A - Pacote 07

- Criado o bounded context `domain.organization`.
- Adicionado agregado `Organization` com evento `OrganizationCreated`.
- Criados value objects de codigo, nome, abreviatura, cidade, estado e pais.
- Adicionado contrato `IOrganizationRepository` e specification `OrganizationCodeAlreadyExists`.
- Criados testes unitarios completos do contexto Organization.

## Sprint 0.2A - Pacote 06

- Criado o contexto de dominio militar inicial.
- Adicionado o agregado `MilitaryPerson` com ciclo de vida, contato e troca de posto/graduacao.
- Criados value objects para identificacao militar, CPF, telefone, nome completo, status e rank.
- Adicionado evento `MilitaryRegistered` e contrato `IMilitaryRepository`.
- Criados testes unitarios para registro, validacoes e eventos do dominio militar.

## Sprint 0.2A - Pacote 05

- Criados contratos de dominio para repository e Unit of Work.
- Adicionados objetos comuns de aplicacao para paginacao, filtros e ordenacao.
- Criada infraestrutura SQLAlchemy definitiva com repository base, session context,
  transaction manager e Unit of Work.
- Adicionados testes unitarios e de integracao para persistencia transacional.

## Sprint 0.2A - Pacote 04

- Criado o Shared Kernel da aplicacao com Entity, AggregateRoot, ValueObject e Identity.
- Adicionados Result Pattern, Notification Pattern, Guard Clauses e Specification Pattern.
- Criado DomainEvent e EventDispatcher sincrono com logging de erros.
- Adicionadas excecoes DomainException e ValidationException.
- Criado container simples de injecao de dependencias em `bootstrap/container.py`.
