# Decisoes Arquitetonicas

## Sprint 0.3 - Base Enterprise

### Clean Architecture como regra de dependencia

O SIGESM Enterprise mantem o dominio independente de infraestrutura e interface.
As camadas externas podem conhecer contratos internos, mas o dominio nao deve
importar SQLAlchemy, PySide6, banco de dados, arquivos de tela ou adapters.

### Bounded Contexts no dominio

Os modulos de negocio permanecem separados por contexto: `military`,
`organization`, `service_scale` e `service_exchange`. Essa divisao evita um
modelo de dominio unico e grande demais, permitindo evolucao por areas
operacionais.

### Persistencia como adapter

Contratos de repository e Unit of Work ficam no dominio. SQLAlchemy fica
concentrado em `infrastructure.persistence.sqlalchemy`, incluindo repository
base, session context, transaction manager e unit of work concreto.

### Excecoes padronizadas

Todas as excecoes corporativas herdam de `SIGESMException`. A hierarquia oficial
e formada por `ApplicationException`, `DomainException`,
`InfrastructureException`, `ValidationException`, `SecurityException` e
`ConfigurationException`.

### Result Pattern e Notification Pattern

O Shared Kernel mantem `Result`, `Notification`, guard clauses e specifications
como mecanismos padrao para respostas de dominio e validacoes acumuladas. Engines
e policies devem preferir objetos de resultado imutaveis quando a decisao
precisar retornar sucesso, falha, motivos, avisos ou metadados.

### Validacao automatizada obrigatoria

A base arquitetural deve permanecer aprovada por pytest, Ruff, Black e MyPy
strict. Violacoes de formatacao, tipagem ou testes quebrados bloqueiam a
continuidade das proximas sprints.

### Dependencias mantidas

As dependencias atuais foram preservadas porque correspondem a capacidades ja
presentes na base: PySide6 para interface, SQLAlchemy e Alembic para
persistencia, psycopg para compatibilidade PostgreSQL, pydantic e
pydantic-settings no modulo `sigesm`, python-dotenv para ambiente e ferramentas
de desenvolvimento para validacao e empacotamento.

## ADR-0004 - Contagem Compartilhada e Prioridade de Servico

Militares podem estar habilitados para varios servicos. Servicos pertencentes ao
mesmo grupo de contagem compartilham a mesma fila de folga para cada tipo de
escala. A contagem oficial passa a ser definida por militar, grupo de contagem e
tipo de escala.

A geracao automatica devera ordenar servicos por prioridade antes de selecionar
candidatos. A antiguidade militar sera aplicada depois de elegibilidade,
restricoes, descanso minimo e maior quantidade de dias sem servico, usando data
da promocao atual, data de praca, data de nascimento e sorteio auditavel em
empate absoluto.
