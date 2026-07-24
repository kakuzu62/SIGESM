# ADR-001 - Modelo Formal de Perfis

## Status

Aceita.

## Contexto

A STS-001F inicia a autorizacao formal do SIGESM sem ainda implementar
permissoes granulares.

## Decisao

Perfis sao dados formais do Identity Context por meio da entidade `Role`.
Usuarios recebem zero ou mais roles por associacao muitos-para-muitos.

O perfil Administrador e identificado por `Role.normalized_name`, nunca por
username, e-mail, nome de botao ou heuristica de UI.

## Consequencias

- a protecao do ultimo administrador ativo passa a ser confiavel;
- a STS-001G podera adicionar permissoes sobre a mesma base;
- a UI continua sem politica de autorizacao embutida;
- seeds devem ser idempotentes.
