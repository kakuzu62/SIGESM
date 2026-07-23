# ADR-0004: Shared Rest Counter and Service Priority

## Status

Aceita.

## Contexto

Militares podem estar habilitados para mais de um servico operacional. Alguns
servicos disputam o mesmo conjunto de militares e devem consumir a mesma fila de
folga. Tratar cada servico como uma fila independente faria um militar parecer
mais descansado para um servico logo apos ter cumprido outro servico equivalente.

Tambem existe prioridade operacional entre servicos. A geracao deve resolver
primeiro os servicos mais criticos para evitar que um militar apto seja
selecionado por uma funcao de menor prioridade antes de uma funcao essencial.

## Decisao

O SIGESM adotara grupos de contagem de folga. A contagem sera vinculada a:

```text
Militar + Grupo de Contagem de Folga + Tipo de Escala
```

Um servico pertence a um grupo de contagem. Quando um militar cumpre servico em
um grupo, a contagem daquele grupo e daquele tipo de escala e reiniciada. Outros
servicos do mesmo grupo passam a considerar essa nova contagem.

Escalas distintas, como PRETA e VERMELHA, podem manter contagens independentes.
O reinicio em uma escala nao altera automaticamente o contador da outra.

Cada tipo de servico tera prioridade de geracao configuravel. Numeros menores
representam maior prioridade. O motor de escala deve gerar primeiro os servicos
mais prioritarios, reservar os militares selecionados durante a simulacao e
validar a escala completa antes da confirmacao.

## Antiguidade Militar

Para militares do mesmo posto ou graduacao, a chave de antiguidade sera:

1. Data da promocao atual, com prioridade para quem foi promovido primeiro.
2. Data de praca, com prioridade para quem ingressou primeiro.
3. Data de nascimento, com prioridade para quem nasceu primeiro.
4. Sorteio automatico auditavel, apenas em empate absoluto.

A antiguidade nao substitui a regra de folga. Ela atua como criterio ordenado de
decisao ou desempate apos elegibilidade, descanso obrigatorio e maior quantidade
de dias sem servico.

## Ordem de Selecao

O pipeline de selecao deve respeitar:

1. Prioridade do servico.
2. Compatibilidade do militar com o servico.
3. Restricoes e indisponibilidades.
4. Descanso minimo obrigatorio.
5. Maior quantidade de dias sem servico.
6. Antiguidade militar.
7. Sorteio auditavel em empate absoluto.

## Estruturas Previstas

- `MilitaryServiceQualification`: vincula militar a tipos de servico permitidos.
- `ServiceRestGroup`: define grupos de contagem compartilhada.
- `ServiceType`: define servico, grupo de contagem e prioridade de geracao.
- `MilitaryRestCounter`: registra contador por militar, grupo e tipo de escala.

## Consequencias

- O cadastro militar precisara armazenar data de promocao atual, data de praca,
  data de nascimento e servicos habilitados.
- O contexto de escalas devera calcular descanso por grupo de contagem, nao
  apenas por nome de servico.
- A geracao automatica devera processar servicos por prioridade antes de
  escolher candidatos.
- Vendas, trocas, afastamentos e execucao real deverao atualizar ou preservar
  contadores conforme o evento operacional aplicavel.
- A regra sera incorporada futuramente em Organization, Military e ServiceScale.
