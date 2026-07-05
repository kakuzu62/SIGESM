# Changelog

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
