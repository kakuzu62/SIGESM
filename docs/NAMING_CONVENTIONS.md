# Naming Conventions

## Arquivos e Pacotes

- Arquivos Python em `snake_case.py`.
- Pacotes em `snake_case`.
- Documentos em `UPPER_SNAKE_CASE.md` quando forem referencias oficiais.

## Classes

- Classes em `PascalCase`.
- Interfaces e contratos com prefixo `I` quando forem contratos de dominio.
- Exceptions terminam com `Exception`.

## Entidades e Value Objects

- Entidades usam nomes do negocio: `MilitaryPerson`, `ServiceScale`.
- Value Objects usam nomes substantivos: `CPF`, `Rank`, `ServiceDate`.

## Repositories

- Contratos: `I<Aggregate>Repository`.
- Implementacoes: `<Technology><Aggregate>Repository` quando houver adapter
  concreto.

## Use Cases

- Padrao: verbo + objeto, por exemplo `RegisterMilitaryUseCase`.
- Commands: `<Action><Target>Command`.
- Queries: `<ReadIntent>Query`.
- Handlers: `<CommandOrQuery>Handler`.

## Eventos

- Eventos no passado: `MilitaryRegistered`, `ScaleGenerated`.
- Arquivos em snake_case com o mesmo significado: `military_registered.py`.

## Testes

- Arquivos: `test_<subject>.py`.
- Funcoes: `test_<behavior>`.
- Testes de dominio devem descrever regra e resultado esperado.

## Migrations

- Nome curto, com verbo e objeto: `create_military_tables`.
- Evitar nomes genericos como `update_tables`.
