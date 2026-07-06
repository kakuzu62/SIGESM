# ADR-0001: Clean Architecture como base obrigatoria

## Status

Aceita.

## Contexto

O SIGESM Enterprise precisa crescer por varios meses sem misturar regra de
negocio, interface grafica, banco de dados e detalhes operacionais.

## Decisao

Adotar Clean Architecture como regra de dependencia. O dominio fica no centro e
nao importa infraestrutura, banco ou UI. Application orquestra casos de uso sem
conhecer presentation. Infrastructure implementa adapters concretos.

## Consequencias

- Regras de negocio permanecem testaveis sem banco ou interface.
- Adapters podem mudar com impacto controlado.
- Revisoes devem bloquear imports indevidos entre camadas.
