# STS-001A - Gestao de Usuarios: Listagem

## Status

Aprovada para implementacao.

## Epico

EP-01 - Administracao.

## Release

2.1 - User Management.

## Objetivo

Entregar a primeira funcionalidade completa visivel ao usuario autenticado:
abrir o modulo `Usuarios`, visualizar a tabela, pesquisar, ordenar, paginar,
atualizar a lista e abrir os formularios placeholder de novo usuario e edicao.

## Escopo

Incluido:

- listagem paginada de usuarios;
- pesquisa incremental;
- ordenacao por coluna;
- atualizacao manual da lista;
- abertura do formulario de novo usuario sem persistencia;
- abertura do formulario de edicao carregando dados sem persistencia;
- integracao ao menu lateral do Desktop Platform.

Fora do escopo:

- criar usuario;
- editar usuario;
- ativar/desativar;
- redefinir senha;
- associar perfis;
- auditar alteracoes.

## Regras

- A tela nao pode acessar repositories ou SQLAlchemy diretamente.
- A tela deve depender apenas do ViewModel.
- O ViewModel deve depender apenas da camada Application.
- Nenhum DTO de listagem pode expor senha, hash de senha ou token.
- A listagem deve carregar apenas a pagina atual.

## Experiencia do Usuario

- A tela deve seguir padrao corporativo, com pesquisa no topo, toolbar, tabela e
  paginacao.
- A pesquisa deve estar preparada para debounce futuro.
- O botao `Excluir` deve permanecer desabilitado nesta STS.
- Mensagens de erro devem ser exibidas em area visivel da tela.
