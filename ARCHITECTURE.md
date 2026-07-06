# Arquitetura SIGESM Enterprise

O SIGESM Enterprise segue Clean Architecture com separacao explicita entre
dominio, aplicacao, infraestrutura, apresentacao e kernel compartilhado.

## Camadas

- `src/domain`: bounded contexts, entidades, value objects, eventos,
  specifications, policies, engines e contratos.
- `src/application`: objetos e contratos de aplicacao, sem dependencia de UI.
- `src/infrastructure`: adapters de persistencia, banco, transacoes e integracoes.
- `src/presentation` e `src/sigesm/presentation`: entrada grafica e adapters de
  interface.
- `src/shared`: primitives compartilhadas de DDD e resultados.
- `src/core`: configuracao, logging, database foundation e excecoes corporativas.

## Regras de Dependencia

O dominio nao depende de SQLAlchemy, PySide6 ou infraestrutura. A aplicacao nao
depende de UI. A infraestrutura implementa contratos internos, sem conter regra
de negocio. A apresentacao nao acessa banco diretamente.

## Persistencia

SQLAlchemy 2 fica isolado em `src/infrastructure/persistence/sqlalchemy` e em
componentes de database foundation de `src/core/database`. Contratos estaveis de
repository e Unit of Work ficam em `src/domain/contracts`.

## Governanca

Decisoes arquitetonicas formais estao em `docs/adr/`. Diagramas estao em
`docs/diagrams/`. A qualidade e garantida por Black, Ruff, MyPy strict e PyTest.
