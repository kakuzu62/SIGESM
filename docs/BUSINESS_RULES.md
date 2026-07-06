# Business Rules

Este documento concentra as regras operacionais conhecidas do SIGESM Enterprise.

## Escalas e Servico

- Todo servico operacional padrao possui duracao de 24 horas.
- O descanso minimo padrao entre servicos e de 78 horas.
- A excecao de escala 1x1 so pode ocorrer com autorizacao formal e registro
  auditavel.
- As escalas iniciais sao PRETA e VERMELHA.
- Cada escala pode possuir funcoes diferentes, com requisitos proprios por
  posto ou graduacao.

## Contadores

- O contador de dias sem servico deve ser acompanhado por militar e por escala.
- Militar novo deve possuir contador inicial configuravel por regra de unidade.
- Venda de servico nao altera indevidamente o contador base do comprador.
- Na venda de servico, o vendedor zera normalmente como se tivesse cumprido o
  servico vendido.
- Militar doente, afastado ou formalmente indisponivel nao zera contador apenas
  por estar fora da escala.

## Elegibilidade

- Militar inativo nao pode assumir servico.
- Militar afastado nao pode assumir servico no periodo do afastamento.
- Militar restrito nao pode assumir servico incompatvel com a restricao.
- Funcoes devem respeitar posto, graduacao, qualificacao e restricoes
  individuais.
- Conflitos de servico e designacoes duplicadas devem tornar o militar
  inelegivel.

## Geracao Automatica

- A selecao automatica deve priorizar militares elegiveis.
- Substituicoes devem selecionar o militar mais descansado quando a regra
  operacional exigir.
- Empates devem ser resolvidos por sorteio automatico auditavel ou por criterio
  deterministico registrado.
- Toda decisao automatica deve registrar motivos, parametros e resultado.

## Troca Oficial

- Troca oficial representa permuta real entre dois militares escalados em datas
  diferentes.
- Apos a troca, cada militar assume efetivamente a data do outro.
- O contador de descanso e folga reinicia conforme o dia efetivamente assumido.
- A elegibilidade dos dois militares deve ser validada nos novos dias.
- Descanso minimo deve ser respeitado, salvo excecao formal autorizada.

## Venda de Servico

- Venda de servico representa passagem de servico sem alterar o contador base do
  comprador.
- O comprador assume servico extraordinario.
- A escala original do comprador deve permanecer preservada.
- A elegibilidade operacional do comprador deve ser validada.
- A decisao deve ser auditavel.

## Auditoria

- Decisoes automaticas, excecoes, trocas, vendas, cancelamentos e mudancas de
  parametros devem ser auditados.
- Auditoria deve registrar ator, data, regra aplicada, entrada, saida e motivos.
