# Rule Engine

Catalogo inicial das regras automaticas do SIGESM Enterprise. Este documento
orienta engines, policies e specifications sem implementar novas regras nesta
release.

## Principios

- Toda regra automatica deve ser deterministica ou auditavelmente aleatoria.
- Toda decisao deve retornar motivos, avisos e metadata.
- Regras criticas devem ser testadas isoladamente.
- Excecoes formais devem ser registradas e auditadas.

## Catalogo Inicial

| Codigo | Regra | Contexto | Entrada | Saida | Criticidade |
|---|---|---|---|---|---|
| SCALE_REST_78H | Validar descanso minimo de 78 horas | ServiceScale | militar, historico, data | elegivel ou motivo | Alta |
| SCALE_1X1_EXCEPTION | Permitir excecao formal 1x1 | ServiceScale | autorizacao, data, militar | permitido ou negado | Alta |
| SCALE_ACTIVE_STATUS | Exigir militar ativo | ServiceScale | status militar | elegivel ou motivo | Alta |
| SCALE_NOT_ON_LEAVE | Bloquear militar afastado | ServiceScale, Leave | periodo, data | inelegivel se conflitante | Alta |
| SCALE_NOT_RESTRICTED | Aplicar restricoes individuais | ServiceScale | restricoes, funcao | elegivel ou motivo | Alta |
| ROLE_RANK_ALLOWED | Validar funcao por posto/graduacao | ServiceScale, Military | rank, role | permitido ou negado | Alta |
| SCALE_COMPATIBLE | Validar compatibilidade de escala | ServiceScale | militar, escala | permitido ou negado | Media |
| SERVICE_CONFLICT | Impedir conflito de designacao | ServiceScale | historico, data | inelegivel se conflito | Alta |
| FAIRNESS_DAYS_COUNTER | Priorizar dias sem servico | ServiceScale | contadores | ranking | Media |
| TIE_BREAK_AUDITABLE | Resolver empate por criterio auditavel | ServiceScale | candidatos empatados | selecionado | Alta |
| SWAP_DUAL_ELIGIBILITY | Validar dois militares na troca oficial | ServiceExchange | troca, historico | aprovado ou negado | Alta |
| SALE_BUYER_ELIGIBILITY | Validar comprador na venda de servico | ServiceExchange | comprador, servico | aprovado ou negado | Alta |
| SALE_COUNTER_PRESERVED | Preservar contador base do comprador | ServiceExchange | venda, contador | decisao auditada | Alta |
| SELLER_COUNTER_RESET | Zerar vendedor conforme regra da venda | ServiceExchange | vendedor, servico | contador atualizado futuro | Alta |

## Pipeline Recomendado

1. Carregar contexto operacional.
2. Normalizar entradas.
3. Executar specifications obrigatorias.
4. Executar policies por contexto.
5. Calcular fairness e desempate.
6. Produzir resultado imutavel.
7. Registrar evento de dominio.
8. Registrar auditoria da decisao.

## Auditoria de Decisao

Cada regra automatica deve registrar:

- identificador da execucao;
- regra avaliada;
- entradas relevantes;
- resultado;
- motivos;
- avisos;
- versao da regra;
- ator ou processo originador;
- data e hora.

## Decisoes Pendentes

- Definir versionamento formal de regras.
- Definir formato final de metadata de decisao.
- Definir se regras parametrizaveis ficarao em Settings ou em tabela propria.
- Definir estrategia de sorteio auditavel com semente registrada.
