# UI Guidelines

Diretrizes para a interface desktop em PySide6.

## Padrao Visual

- Interface profissional, objetiva e densa o suficiente para uso operacional.
- Evitar telas decorativas; priorizar leitura, acao rapida e consistencia.
- Usar tema claro e escuro com tokens centralizados de cor, espacamento e fonte.

## Shell e Navegacao

- Shell principal com menu lateral, area de conteudo e barra de status.
- HeaderBar deve conter identidade da aplicacao, usuario autenticado e acoes
  globais.
- SideBar deve expor apenas modulos registrados no `NavigationService`.
- WorkspaceView deve ser a unica area de troca de views de modulo.
- Navegacao por modulos: Dashboard, Organizacao, Militares, Escalas, Trocas,
  Relatorios, Auditoria e Configuracoes.
- Acoes globais devem ficar em locais previsiveis.

## MVVM

- Views PySide6 nao acessam repositories, SQLAlchemy, engines ou regras de
  dominio diretamente.
- Toda acao de tela passa por ViewModel, Controller ou caso de uso da camada
  Application.
- ViewModels podem usar `ObservableObject`, `Command` e lifecycle padrao.
- Widgets devem conter apenas composicao visual e binding de interacao.

## Dashboard

- Exibir pendencias, proximas escalas, alertas de elegibilidade e indicadores.
- Nao substituir relatorios detalhados.

## Formularios

- Campos agrupados por significado operacional.
- Validacao visual imediata quando segura.
- Mensagens claras, sem termos tecnicos desnecessarios.
- Botoes principais sempre distinguiveis dos secundarios.

## Tabelas

- Ordenacao, filtros e paginacao quando houver volume.
- Colunas essenciais visiveis por padrao.
- Acoes de linha devem ser consistentes.

## Dialogos

- Usar dialogos para confirmacoes, detalhes e fluxos curtos.
- Operacoes criticas devem explicar impacto antes da confirmacao.

## Temas

- Temas devem ser aplicados via `ThemeManager`.
- Arquivos QSS devem ficar em `resources/styles` e ter fallback seguro.
- Dark e Light sao obrigatorios; Alto Contraste deve permanecer preparado.

## Mensagens

- Sucesso: indicar resultado.
- Alerta: indicar consequencia.
- Erro: indicar causa e proximo passo.
- Decisoes de elegibilidade devem mostrar todos os motivos relevantes.

## Acessibilidade

- Contraste adequado nos dois temas.
- Navegacao por teclado.
- Foco visual claro.
- Textos objetivos para leitores de tela quando aplicavel.

## Atalhos

- Atalhos devem ser documentados na propria interface.
- Acoes destrutivas nao devem depender apenas de teclado.
