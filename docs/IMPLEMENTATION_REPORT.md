# Relatorio de Implementacao - Release 2.0

## ADR-0004 - Shared Rest Counter and Service Priority

Foi registrada a regra arquitetural de contagem compartilhada de folga e
prioridade de servico. A decisao nao implementa novas funcionalidades, mas passa
a orientar as futuras STSs de Organization, Military e ServiceScale.

Resumo da decisao:

- Um militar pode estar habilitado para varios tipos de servico.
- Servicos do mesmo grupo compartilham o contador de folga.
- A contagem oficial e definida por militar, grupo de contagem e tipo de escala.
- Tipos de servico possuem prioridade configuravel de geracao.
- Antiguidade militar considera data da promocao atual, data de praca, data de
  nascimento e sorteio auditavel em empate absoluto.
- A regra foi documentada em `docs/adr/ADR-0004-shared-rest-counter-service-priority.md`.

## Objetivo

Implementar a primeira plataforma desktop executavel do SIGESM Enterprise,
mantendo a separacao entre Presentation, Application, Domain e Infrastructure.

## Entregas

- Splash screen de inicializacao.
- Tela de login integrada ao Authentication Core.
- Janela principal com header, menu lateral, workspace central e status bar.
- Navegacao entre modulos iniciais com historico de voltar e avancar.
- Dashboard inicial com cards de Militares, Escalas, Organizacoes, Pendencias e
- Auditoria exibindo valores zerados.
- Gerenciamento de tema Light e Dark por QSS em tempo de execucao.
- Estrutura preparada para Alto Contraste.
- Servico de notificacoes da interface.
- Dialogo padrao de mensagens.
- Primitives MVVM para ObservableObject, Command e ViewModel.
- Resource manager desktop.
- Repositories de identidade em memoria para bootstrap local.

## Fluxo de Inicializacao

O entrypoint `src/main.py` delega para `sigesm.main`, que monta o container da
aplicacao e inicia `DesktopApplication`. Durante a inicializacao, o lifecycle
registra logs, a aplicacao exibe a splash screen, executa o health check,
carrega o contexto desktop, aplica o tema padrao e abre o login.

## Autenticacao

O login nao utiliza autenticacao ficticia. A View chama `LoginViewModel`, que
aciona `LoginController` e o use case `AuthenticateUserHandler`. O handler usa
`AuthenticationService`, policies e `PasswordService` do contexto Identity.

Para desenvolvimento local, o container registra repositories em memoria e cria
um usuario administrativo inicial:

- usuario: `admin`
- senha: `Admin#123`

## Arquitetura Visual

O `MainWindow` concentra apenas responsabilidades de shell e recebe
`ShellViewModel`. O shell e dividido em `HeaderBar`, `SideBar`, `WorkspaceView`
e `StatusBar`. A navegacao e controlada por `NavigationService` e
`NavigationHistory`, o workspace por `WorkspaceManager` e os temas por
`ThemeManager`.

As views dos modulos iniciais sao placeholders estruturais. Elas nao acessam
repositories, SQLAlchemy, engines ou regras de dominio diretamente.

## Arquivos Principais

- `src/presentation/framework/application/desktop_application.py`
- `src/presentation/framework/application/application_lifecycle.py`
- `src/sigesm/presentation/qt/app.py`
- `src/presentation/framework/views/login_dialog.py`
- `src/presentation/framework/shell/main_window.py`
- `src/presentation/framework/viewmodels/login_viewmodel.py`
- `src/presentation/framework/controllers/login_controller.py`
- `src/presentation/framework/themes/theme_manager.py`
- `src/presentation/framework/navigation/navigation_service.py`
- `src/presentation/framework/workspace/workspace_manager.py`
- `src/presentation/modules/dashboard/dashboard_view.py`

## Validacoes

Validacoes executadas ao final da release:

- Black.
- Ruff.
- MyPy strict.
- PyTest.

Resultado: suite completa aprovada com 93 testes.

## Observacoes

Nenhuma funcionalidade de negocio nova foi criada nesta release. A entrega cria
a plataforma visual reutilizavel que recebera os modulos funcionais das
proximas releases.
