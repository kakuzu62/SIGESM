# SIGESM Enterprise

SIGESM Enterprise e um sistema corporativo em Python 3.12 para gestao militar,
construido com PySide6, SQLAlchemy 2, Alembic, Clean Architecture e DDD.

## Estado da Fundacao

A Sprint 1.0 consolidou a base para crescimento de longo prazo. A Release 2.0
inaugura a fase visual do produto com uma plataforma desktop executavel em
PySide6, login integrado ao Authentication Core, shell principal, navegacao,
workspace, temas e modulos iniciais.

## Qualidade

Comandos padrao:

```powershell
.\.venv\Scripts\python.exe -m black --check src tests migrations
.\.venv\Scripts\python.exe -m ruff check src tests migrations
.\.venv\Scripts\python.exe -m mypy src tests migrations
.\.venv\Scripts\python.exe -m pytest
```

O pipeline em `.github/workflows/quality.yml` executa as mesmas verificacoes em
pull requests e pushes para `main`.

## Build

O empacotamento inicial com PyInstaller esta preparado em `build/` e `scripts/`.

```powershell
.\scripts\build.ps1
```

```bash
./scripts/build.sh
```

## Sprint 0.3 - Consolidacao Arquitetural

A base da Sprint 0 foi consolidada com auditoria entre camadas, MyPy strict,
Ruff, Black e testes automatizados. O dominio permanece desacoplado de
infraestrutura e interface, os contratos de persistencia nao dependem de
SQLAlchemy e a hierarquia de excecoes foi estabilizada para uso corporativo.

As decisoes arquitetonicas estao registradas em `docs/DECISIONS.md`.

As ADRs formais da Sprint 1.0 estao em `docs/adr/`.

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

## Identidade e Seguranca

O contexto `src/domain/identity` implementa a base inicial de identidade sem
interface grafica. Ele modela usuarios como aggregate roots, roles, permissions,
sessoes, politicas de senha e tentativa de login, servico de hash seguro de
senha e contratos de repositorio. A infraestrutura SQLAlchemy correspondente
fica em `src/infrastructure/persistence/sqlalchemy/identity`.

A Release 1.1 adiciona o nucleo de autenticacao com login, logout, validacao e
renovacao de sessao, recuperacao de senha, auditoria de tentativas e hash
Argon2id para senhas.

## Desktop Framework

O pacote `src/presentation/framework` fornece a base reutilizavel da interface
desktop: shell, navegacao, workspace, dialogos, componentes, temas, recursos,
MVVM, comandos e viewmodels. Ele nao contem regras de negocio nem acesso direto
a repositories ou SQLAlchemy.

## Release 2.0 - Desktop Platform

A aplicacao agora pode ser iniciada por `python src/main.py` ou
`python -m sigesm`. O fluxo visual carrega splash screen, valida a fundacao,
abre a tela de login e, apos autenticacao pelo Authentication Core, exibe a
janela principal do SIGESM.

A plataforma desktop inclui:

- `DesktopApplication` e `ApplicationLifecycle` para startup, shutdown, logs e
  tratamento global de excecoes;
- shell principal com header, menu lateral, workspace central e status bar;
- navegacao com historico entre Dashboard, Organizacoes, Militares, Escalas e
  Configuracoes;
- dashboard inicial com cards de Militares, Escalas, Organizacoes, Pendencias e
- Auditoria exibindo valores zerados ate conexao com os modulos reais;
- troca de tema em tempo de execucao entre Light e Dark via QSS, com estrutura
  preparada para Alto Contraste;
- ViewModels e controllers isolando a interface da camada Application;
- primitives MVVM para `ObservableObject`, `Command` e `ViewModel`;
- repositorios de identidade em memoria para bootstrap local de autenticacao,
  usando o mesmo Authentication Core de producao.

Credenciais locais de desenvolvimento:

- usuario: `admin`
- senha: `Admin#123`

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
