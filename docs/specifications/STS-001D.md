# STS-001D - Ativacao e Desativacao de Usuarios

## Status

Pendente de AR-004.

## Objetivo

Permitir que um administrador ative ou desative usuarios administrativos
existentes pela listagem de usuarios, sem alterar cadastro, senha, perfis,
permissoes, exclusao ou auditoria detalhada.

## Escopo

- selecionar usuario na listagem;
- confirmar ativacao ou desativacao;
- impedir auto-desativacao na camada Application;
- persistir o novo estado por Repository e Unit of Work;
- atualizar a listagem mantendo filtro, ordenacao e pagina;
- rejeitar autenticacao de usuario inativo.

## Fora de Escopo

- redefinicao de senha;
- perfis e permissoes;
- exclusao fisica ou logica;
- auditoria detalhada;
- bloqueio automatico por tentativas;
- controle otimista.

## Regras

- usuario ativo pode ser desativado;
- usuario inativo pode ser ativado;
- solicitar o mesmo estado retorna falha de negocio compreensivel;
- `updated_at` muda apenas quando ha mudanca real;
- ID, nome, login, e-mail, senha, roles, permissoes e `created_at` sao preservados;
- o ator autenticado nao pode desativar a propria conta;
- protecao do ultimo administrador fica pendente ate roles/permissoes serem confiaveis.
