# Product Backlog

## Foundation

| Feature | Prioridade | Dependencias |
|---|---|---|
| CI completo | Alta | Sprint 1.0 |
| ADRs e diagramas | Alta | Sprint 1.0 |
| Padroes de codigo | Alta | Sprint 1.0 |

## Identity

| Feature | Prioridade | Dependencias |
|---|---|---|
| Login | Alta | Foundation |
| Usuarios | Alta | Foundation |
| Criacao de usuarios | Alta | Usuarios |
| Edicao de usuarios | Alta | Usuarios |
| Ativacao e desativacao de usuarios | Alta | Usuarios |
| Redefinicao de senha | Alta | Usuarios |
| Atribuicao de perfis | Alta | Usuarios |
| Perfis e permissoes | Alta | Usuarios |

## Organization

| Feature | Prioridade | Dependencias |
|---|---|---|
| Cadastro de organizacao | Alta | Foundation |
| Parametros por organizacao | Media | Settings |

## Military Registry

| Feature | Prioridade | Dependencias |
|---|---|---|
| Cadastro de militar | Alta | Organization |
| Restricoes individuais | Alta | Military |
| Historico funcional | Media | Audit |

## Service Scale

| Feature | Prioridade | Dependencias |
|---|---|---|
| Cadastro de funcoes | Alta | Military |
| Elegibilidade | Alta | Military, Leave |
| Geracao automatica | Alta | Elegibilidade |

## Service Exchange

| Feature | Prioridade | Dependencias |
|---|---|---|
| Troca oficial | Alta | Service Scale |
| Venda de servico | Alta | Service Scale |

## Leave Management

| Feature | Prioridade | Dependencias |
|---|---|---|
| Cadastro de afastamento | Alta | Military |
| Integracao com escala | Alta | Service Scale |

## Audit

| Feature | Prioridade | Dependencias |
|---|---|---|
| Registro de decisoes | Alta | Foundation |
| Consulta de auditoria | Alta | Identity |

## Reports

| Feature | Prioridade | Dependencias |
|---|---|---|
| Relatorio de escala | Media | Service Scale |
| Relatorio de auditoria | Media | Audit |

## Desktop UI

| Feature | Prioridade | Dependencias |
|---|---|---|
| Shell principal | Alta | Identity |
| Telas de cadastro | Alta | Organization, Military |
| Dashboard | Media | Reports |

## Deployment

| Feature | Prioridade | Dependencias |
|---|---|---|
| Build Windows | Alta | Desktop UI |
| Backup e restauracao | Alta | Database |
