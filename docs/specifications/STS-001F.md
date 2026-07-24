# STS-001F - Atribuicao de Perfis aos Usuarios

## Status

Pendente de AR-006.

## Objetivo

Permitir que um administrador atribua e remova perfis existentes de usuarios
administrativos, sem implementar permissoes granulares, cadastro completo de
perfis, auditoria detalhada ou politicas avancadas de autorizacao.

## Escopo

- abrir gestao de perfis a partir da listagem de usuarios;
- listar perfis disponiveis;
- marcar perfis atualmente atribuidos;
- atribuir e remover perfis;
- proteger o ultimo Administrador ativo;
- persistir associacoes User <-> Role;
- atualizar a listagem mantendo filtro, ordenacao e pagina.

## Regras

- usuario pode possuir zero ou mais perfis;
- perfis duplicados sao rejeitados;
- perfis inexistentes sao rejeitados;
- perfis inativos nao podem ser atribuidos;
- `updated_at` muda apenas quando ha alteracao real;
- ID, nome, username, e-mail, senha, estado e `created_at` sao preservados;
- a protecao administrativa usa perfil formal `Administrador`, usuario ativo e
  associacao persistida.

## Fora de Escopo

- CRUD completo de perfis;
- permissoes granulares;
- associacao perfil-permissao;
- autorizacao centralizada de telas;
- auditoria detalhada;
- heranca de perfis.
