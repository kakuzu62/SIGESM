# Changelog

## Release 2.0 - Desktop Platform

- Criada a primeira plataforma visual executavel do SIGESM Enterprise.
- Integrado `python src/main.py` ao bootstrap principal `sigesm.main`.
- Adicionados `DesktopApplication` e `ApplicationLifecycle` para startup,
  shutdown, logs e tratamento de excecoes.
- Adicionado fluxo PySide6 com splash screen, health check, login e janela
  principal.
- Criados `LoginDialog`, `LoginViewModel` e `LoginController` integrados ao
  `AuthenticateUserHandler`.
- Criado shell principal com `HeaderBar`, `SideBar`, `WorkspaceView`,
  `StatusBar`, `ShellViewModel` e troca de tema em tempo de execucao.
- Adicionados `DesktopContext`, `ThemeManager` e `NotificationService`.
- Criados `NavigationItem`, `NavigationService` e `NavigationHistory`.
- Criados primitives MVVM `ObservableObject`, `Command` e `ViewModel`.
- Adicionados `QssLoader`, `DesktopResourceManager`, QSS dark/light e estrutura
  de recursos desktop.
- Criados modulos iniciais de Dashboard, Organizacoes, Militares, Escalas e
  Configuracoes com views e viewmodels.
- Adicionados repositories de identidade em memoria para bootstrap local de
  autenticacao sem bypass de regra de dominio.
- Criados testes unitarios para navegacao, workspace, notificacoes e recursos.

## Release 1.1 - Authentication Core

- Adicionado `AuthenticationService` ao contexto Identity.
- Criadas entidades `AuthenticationSession`, `RefreshSession`,
  `PasswordResetRequest` e `AuthenticationAttempt`.
- Migrado `PasswordService` para Argon2id com `argon2-cffi`.
- Criados use cases de autenticar, sair, alterar senha autenticada, solicitar e
  confirmar recuperacao de senha, validar sessao e renovar sessao.
- Criada persistencia SQLAlchemy para sessoes, refresh sessions, reset de senha
  e tentativas de login.
- Criado Desktop Framework reutilizavel em `src/presentation/framework`.
- Adicionados testes para login valido, senha invalida, usuario bloqueado,
  sessao expirada, alteracao de senha, recuperacao de senha e renovacao.

## Release 1.0 - Identity Context

- Criado o bounded context `domain.identity`.
- Adicionados agregados e entidades `User`, `Role`, `Permission` e
  `UserSession`.
- Criados value objects para username, email, hash de senha, codigo de permissao
  e status de sessao.
- Criados eventos de dominio para criacao, ativacao, desativacao, troca de senha
  e falha de login.
- Criadas policies de senha e tentativa de login.
- Criados services de senha e permissao.
- Criados commands, queries e DTOs de application para Identity.
- Criados models, mappers e repositories SQLAlchemy para Identity.
- Criados testes unitarios e de integracao do contexto.

## Release 0.5 - Data Architecture

- Criada arquitetura de dados completa em `docs/DATA_ARCHITECTURE.md`.
- Expandido `docs/DATABASE_MODEL.md` com convencoes fisicas, Alembic,
  auditoria, timestamps, soft delete e historico.
- Criado `docs/RULE_ENGINE.md` com catalogo inicial de regras automaticas.
- Criado `docs/EVENT_STORMING.md` com comandos, eventos, agregados e policies.
- Criados diagramas `docs/diagrams/DATABASE_ER.md` e
  `docs/diagrams/EVENT_FLOW.md`.
- Registrados riscos tecnicos e decisoes pendentes.
- Nenhuma tabela, migration ou funcionalidade de negocio foi criada.

## Release 0.4 - Enterprise Blueprint

- Criada documentacao executiva e arquitetural oficial da fundacao Enterprise.
- Adicionados documentos de dominio, eventos, regras de negocio, casos de uso,
  UI, banco, API, nomes, codigo, seguranca, testes, deployment, backlog e
  roadmap.
- Criados diagramas oficiais em Mermaid com nomes padronizados em
  `docs/diagrams/`.
- Atualizado `docs/IMPLEMENTATION_REPORT.md` com o resumo da Release 0.4.
- Nenhuma funcionalidade de negocio foi implementada ou alterada.

## Sprint 1.0 - Enterprise Foundation

- Realizada revisao geral da fundacao arquitetural existente.
- Padronizado bootstrap para usar logging em vez de saida direta no console.
- Criados ADRs formais em `docs/adr/`.
- Criados diagramas arquitetonicos em `docs/diagrams/`.
- Criado pipeline de CI com Black, Ruff, MyPy e PyTest.
- Criados documentos `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md` e
  `.github/CODEOWNERS`.
- Criada estrutura inicial de build PyInstaller em `build/` e `scripts/`.
- Atualizados README, ARCHITECTURE e relatorio de implementacao.

## Sprint 0.3 - Consolidacao da Arquitetura

- Realizada auditoria de dependencias entre `domain`, `application`,
  `infrastructure`, `presentation` e `shared`.
- Removida dependencia de SQLAlchemy do contrato de Unit of Work do dominio.
- Consolidada a hierarquia de excecoes corporativas em `core.exceptions`.
- Aplicados Ruff, Black e MyPy strict em todo o codigo do projeto.
- Corrigidas tipagens em testes e no modulo legado `sigesm`.
- Registradas decisoes arquitetonicas em `docs/DECISIONS.md`.
- Validada a base com a suite completa de testes automatizados.

## Sprint 0.2A - Pacote 11

- Criado o bounded context `domain.service_exchange`.
- Adicionadas entidades `OfficialSwap` e `ServiceSale`.
- Criados motores de validacao para troca oficial e venda de servico.
- Adicionadas policies de decisao auditavel e eventos de aprovacao/rejeicao.
- Criado contrato `IServiceExchangeRepository`.
- Criados testes unitarios para troca oficial, excecao formal e venda de servico.

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
