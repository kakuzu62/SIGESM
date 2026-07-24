# STS-001E - Redefinicao de Senha

## Status

Pendente de AR-005.

## Objetivo

Permitir que um administrador redefina a senha de qualquer usuario do sistema,
sem misturar o fluxo com edicao cadastral, perfis, permissoes, recuperacao por
e-mail, MFA, tokens ou historico de senhas.

## Escopo

- selecionar usuario na listagem;
- abrir dialogo especifico de redefinicao de senha;
- informar nova senha e confirmacao;
- validar confirmacao na Presentation;
- validar politica de senha pelo `PasswordService`;
- persistir apenas hash seguro;
- limpar campos sensiveis apos sucesso ou cancelamento;
- atualizar a listagem mantendo filtro, ordenacao e pagina.

## Regras

- senha nunca trafega em DTO de saida;
- hash nunca trafega para View, ViewModel ou sinais;
- o dominio nao conhece `confirm_password`;
- `User.change_password()` preserva ID, nome, login, e-mail, estado, roles,
  permissoes e `created_at`;
- `updated_at` e atualizado no sucesso.

## Fora de Escopo

- troca de senha pelo proprio usuario;
- recuperacao por e-mail;
- token de redefinicao;
- MFA;
- expiracao de senha;
- historico de senhas;
- invalidacao de sessoes ativas.
