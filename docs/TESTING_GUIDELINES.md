# Testing Guidelines

## Tipos de Teste

- Unitarios: regras de dominio, value objects, policies, specifications e
  engines.
- Aplicacao: use cases, commands, queries e handlers.
- Integracao: repositories, Unit of Work, migrations e adapters.
- Infraestrutura: banco, configuracao e logging.

## Fixtures

- Fixtures devem ser pequenas e explicitas.
- Evitar dados magicos compartilhados demais.
- Bancos de teste devem ser temporarios.

## Cobertura

- Regras de negocio criticas exigem teste de sucesso e falha.
- Bugs corrigidos devem ganhar teste de regressao.
- Cobertura minima sera definida antes da primeira release operacional.

## Nomenclatura

- Arquivos: `test_<modulo>.py`.
- Funcoes: `test_<comportamento>`.
- Evitar nomes genericos como `test_success`.

## Criterios de Aceitacao

- PyTest deve passar.
- MyPy strict deve passar.
- Ruff e Black devem passar.
- Testes nao devem depender de ordem de execucao.
