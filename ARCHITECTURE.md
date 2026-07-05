# Arquitetura SIGESM Enterprise

O SIGESM Enterprise segue Clean Architecture com separacao entre dominio,
aplicacao, infraestrutura e apresentacao.

## Dominio

O dominio define contratos estaveis em `src/domain/contracts`, incluindo
`IRepository` e `IUnitOfWork`. Esses contratos nao dependem de detalhes de banco
ou framework.

## Aplicacao

`src/application/common` contem objetos reutilizaveis para consultas, como
paginacao, ordenacao e filtros tipados.

## Infraestrutura

`src/infrastructure/persistence/sqlalchemy` implementa os contratos de
persistencia com SQLAlchemy 2.x. A infraestrutura inclui repository base,
contexto de sessao, gerenciador transacional com nested transactions/savepoints
e Unit of Work.

## Configuracao

A configuracao de banco e pool e obtida por `core.config.settings`. Nenhum
adapter de persistencia le variaveis de ambiente diretamente.
