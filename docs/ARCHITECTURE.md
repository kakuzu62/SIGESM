# Arquitetura do Dominio

## Contexto Militar

O contexto `domain.military` concentra o nucleo militar do SIGESM Enterprise.
Ele utiliza DDD com `MilitaryPerson` como AggregateRoot e value objects para
identificacao militar, CPF, nome completo, telefone, posto/graduacao e status.

O registro de um militar emite `MilitaryRegistered`, permitindo que casos de uso
futuros reajam ao evento sem acoplar regras de dominio a infraestrutura.

## Contexto Organization

O contexto `domain.organization` representa organizacoes militares e suas regras
de identidade institucional. `Organization` e um AggregateRoot com codigo,
nome, abreviatura e localizacao. O contexto publica `OrganizationCreated` e
define `IOrganizationRepository` para consultas por codigo sem acoplar dominio a
SQLAlchemy.

## Contexto Service Scale

O contexto `domain.service_scale` concentra as regras de escala de servico.
`ServiceScale` e o AggregateRoot responsavel por funcoes de servico e
designacoes. `ServiceAssignment` representa uma designacao de militar para um
servico de 24 horas. O contexto possui policies e specifications para descanso
minimo, disponibilidade e desempate deterministico auditavel.

O `EligibilityEngine` e um domain service puro. Ele recebe militar, escala,
funcao, historico e data, executa uma `EligibilityPolicy` com specifications em
pipeline e retorna `EligibilityResult` imutavel com todos os motivos encontrados.
O motor registra logs de decisao e emite eventos sem depender de UI ou banco.

O `ScaleGenerationEngine` orquestra a geracao automatica usando Strategy Pattern
para regras por tipo de escala, Policy Pattern para o fluxo de geracao,
services de fairness e descanso, e o Eligibility Engine para validar candidatos.
O resultado da geracao e imutavel e contem estatisticas, eventos e descartes.
