# Arquitetura do Dominio

## Consolidacao da Sprint 0.3

A arquitetura do SIGESM Enterprise esta organizada em camadas independentes:

- `domain`: regras de negocio, entidades, value objects, eventos, policies,
  specifications e contratos puros.
- `application`: objetos de aplicacao e orquestracao sem dependencia de UI.
- `infrastructure`: adapters concretos, persistencia SQLAlchemy, sessoes,
  transacoes e integracoes externas.
- `presentation`: interface grafica e adaptadores de entrada.
- `shared`: kernel compartilhado com primitives de DDD e suporte transversal.

A auditoria da Sprint 0.3 removeu dependencia de SQLAlchemy do contrato
`domain.contracts.IUnitOfWork`. Tipos e detalhes do banco ficam restritos a
`infrastructure.persistence`, enquanto o dominio continua expressando apenas os
contratos necessarios para regras e casos de uso.

As excecoes seguem uma hierarquia unica em `core.exceptions`: `SIGESMException`
como base, com especializacoes para `ApplicationException`, `DomainException`,
`InfrastructureException`, `ValidationException`, `SecurityException` e
`ConfigurationException`.

O projeto e validado por MyPy strict, Ruff, Black e pytest. A formatacao e a
tipagem fazem parte da definicao de pronto da base arquitetural.

## Preparacao Enterprise da Sprint 1.0

A Sprint 1.0 adiciona governanca e operacao de engenharia sobre a base existente:

- ADRs formais em `docs/adr/`.
- Diagramas de contexto, camadas, dominio, infraestrutura, banco e modulos em
  `docs/diagrams/`.
- GitHub Actions para Black, Ruff, MyPy e PyTest.
- Documentos de contribuicao, conduta, seguranca e ownership.
- Build PyInstaller versionado em `build/` e `scripts/`.

Nenhuma nova funcionalidade de negocio foi adicionada. A mudanca consolida
estrutura, padroes e capacidade de evolucao.

## Contexto Identity

O contexto `domain.identity` e o primeiro modulo funcional da Release 1.0. Ele
segue DDD com `User` como AggregateRoot e `Role`, `Permission` e `UserSession`
como entidades. Value objects normalizam username, email, hash de senha, codigo
de permissao e status de sessao.

As regras de senha e tentativa de login ficam em policies de dominio. O hash e a
verificacao de senha ficam em `PasswordService`, usando PBKDF2-SHA256 com salt.
Application define commands, queries e DTOs sem depender de UI. A persistencia
SQLAlchemy fica isolada em `infrastructure.persistence.sqlalchemy.identity`, com
models, repositories e mapper explicito entre dominio e banco.

### Authentication Core

A Release 1.1 expande Identity com `AuthenticationService`,
`AuthenticationSession`, `RefreshSession`, `PasswordResetRequest` e
`AuthenticationAttempt`. Tokens de acesso, refresh e reset sao opacos para o
cliente e persistidos somente como hash SHA-256. Senhas usam Argon2id por meio
de `argon2-cffi`, mantendo comparacao segura pela biblioteca de hashing.

As policies de tentativa de login sao configuraveis para bloqueio futuro. A
auditoria inicial de autenticacao e representada por `AuthenticationAttempt`.
Application expoe use cases de autenticar, sair, alterar senha, solicitar e
confirmar recuperacao de senha, validar sessao e renovar sessao.

## Desktop Framework

O pacote `presentation.framework` cria uma infraestrutura reutilizavel para a UI
PySide6 futura. Ele contem primitivas de shell, navegacao, workspace, dialogos,
componentes, temas, resources, commands, MVVM e viewmodels. O framework nao
contem regras de negocio e nao acessa banco.

### Desktop Platform

A Release 2.0 transforma o framework em uma plataforma desktop executavel.
`DesktopApplication` cria o `QApplication`, aplica lifecycle, exibe splash
screen, valida a saude da fundacao e abre o fluxo de login. O entrypoint
`python src/main.py` delega para `sigesm.main`, que monta o container e aciona a
plataforma.

O login usa `LoginDialog`, `LoginViewModel` e `LoginController`, que chamam o
use case `AuthenticateUserHandler`. A View nao conhece repositories, engines ou
SQLAlchemy. Para bootstrap local, a composicao registra repositories de
identidade em memoria e cria um usuario administrativo de desenvolvimento com
senha protegida pelo `PasswordService`.

O `MainWindow` fica em `presentation.framework.shell` e recebe
`ShellViewModel`. O shell e dividido em `HeaderBar`, `SideBar`, `WorkspaceView`
e `StatusBar`. A navegacao e controlada por `NavigationService` e
`NavigationHistory`, enquanto o carregamento de telas fica no
`WorkspaceManager`. Os modulos iniciais `login`, `dashboard`, `organization`,
`military`, `scale` e `settings` possuem views e viewmodels proprios, mantendo o
contrato visual pronto para as proximas releases.

O `ThemeManager` usa `QssLoader` para carregar `dark.qss` e `light.qss`, aplica
temas em tempo de execucao e mantem a estrutura preparada para Alto Contraste.
Recursos visuais sao resolvidos por `DesktopResourceManager`, sem acesso direto
a infraestrutura de persistencia.

## Contexto Militar

O contexto `domain.military` concentra o nucleo militar do SIGESM Enterprise.
Ele utiliza DDD com `MilitaryPerson` como AggregateRoot e value objects para
identificacao militar, CPF, nome completo, telefone, posto/graduacao e status.

O registro de um militar emite `MilitaryRegistered`, permitindo que casos de uso
futuros reajam ao evento sem acoplar regras de dominio a infraestrutura.

## Contexto Organization

O contexto `domain.organization` representa organizacoes militares e suas regras
de identidade institucional. `Organization` e um AggregateRoot com codigo,
nome, abreviatura e localizacao. O contexto publica `OrganizationCreated` e
define `IOrganizationRepository` para consultas por codigo sem acoplar dominio a
SQLAlchemy.

## Contexto Service Scale

O contexto `domain.service_scale` concentra as regras de escala de servico.
`ServiceScale` e o AggregateRoot responsavel por funcoes de servico e
designacoes. `ServiceAssignment` representa uma designacao de militar para um
servico de 24 horas. O contexto possui policies e specifications para descanso
minimo, disponibilidade e desempate deterministico auditavel.

O `EligibilityEngine` e um domain service puro. Ele recebe militar, escala,
funcao, historico e data, executa uma `EligibilityPolicy` com specifications em
pipeline e retorna `EligibilityResult` imutavel com todos os motivos encontrados.
O motor registra logs de decisao e emite eventos sem depender de UI ou banco.

O `ScaleGenerationEngine` orquestra a geracao automatica usando Strategy Pattern
para regras por tipo de escala, Policy Pattern para o fluxo de geracao,
services de fairness e descanso, e o Eligibility Engine para validar candidatos.
O resultado da geracao e imutavel e contem estatisticas, eventos e descartes.

## Contexto Service Exchange

O contexto `domain.service_exchange` separa troca oficial de venda de servico.
`OfficialSwap` representa troca real entre dois militares e valida elegibilidade
dos dois nos dias assumidos. `ServiceSale` representa servico extraordinario
assumido pelo comprador, preservando seu contador original e registrando a
zeragem normal do vendedor. Ambos usam engines e policies de dominio, sem UI ou
infraestrutura.
