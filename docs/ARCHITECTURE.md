# Arquitetura do Dominio

## Contexto Militar

O contexto `domain.military` concentra o nucleo militar do SIGESM Enterprise.
Ele utiliza DDD com `MilitaryPerson` como AggregateRoot e value objects para
identificacao militar, CPF, nome completo, telefone, posto/graduacao e status.

O registro de um militar emite `MilitaryRegistered`, permitindo que casos de uso
futuros reajam ao evento sem acoplar regras de dominio a infraestrutura.
