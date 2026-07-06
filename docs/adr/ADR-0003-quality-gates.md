# ADR-0003: Quality gates obrigatorios

## Status

Aceita.

## Contexto

Uma base Enterprise precisa impedir regressao estrutural, formatacao divergente,
tipagem incompleta e testes quebrados.

## Decisao

Black, Ruff, MyPy strict e PyTest sao obrigatorios localmente e no CI. Pull
requests e pushes para `main` executam a pipeline `.github/workflows/quality.yml`.

## Consequencias

- Codigo inconsistente nao deve entrar em `main`.
- Tipagem passa a ser parte do contrato do projeto.
- Testes automatizados documentam comportamento esperado.
