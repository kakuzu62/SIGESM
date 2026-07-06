# Use Cases

Casos de uso iniciais previstos para orientar o desenvolvimento.

## Autenticacao

- Entrar no sistema com usuario e senha.
- Encerrar sessao.
- Bloquear acesso apos tentativas invalidas.

## Gestao de Usuarios

- Criar usuario.
- Ativar e desativar usuario.
- Redefinir senha.
- Vincular usuario a militar quando aplicavel.

## Gestao de Perfis

- Criar perfil.
- Associar permissoes.
- Remover permissoes.
- Listar usuarios por perfil.

## Gestao de Permissoes

- Consultar permissoes disponiveis.
- Validar acesso a telas, acoes e relatorios.
- Auditar alteracoes de permissao.

## Cadastro de Organizacao

- Cadastrar organizacao militar.
- Validar codigo unico.
- Atualizar dados institucionais.

## Cadastro de Militar

- Registrar militar.
- Validar CPF, nome completo, identificacao militar e telefone.
- Alterar posto ou graduacao.
- Ativar ou desativar militar.

## Cadastro de Restricoes

- Registrar restricao individual.
- Definir periodo e motivo.
- Consultar restricoes ativas.

## Cadastro de Funcoes

- Criar funcao de servico.
- Definir requisitos por posto, graduacao e qualificacao.
- Ativar ou desativar funcao.

## Geracao de Escala

- Selecionar data, escala e funcao.
- Avaliar candidatos.
- Aplicar descanso, restricoes e justica.
- Gerar escala com auditoria.

## Validacao de Elegibilidade

- Avaliar militar para servico especifico.
- Retornar todos os motivos de inelegibilidade.
- Registrar decisao.

## Troca Oficial

- Solicitar troca entre dois militares.
- Validar elegibilidade nos novos dias.
- Aprovar ou rejeitar com motivo.

## Venda de Servico

- Solicitar venda.
- Validar comprador.
- Registrar servico extraordinario.
- Preservar contador base do comprador.

## Afastamento

- Cadastrar afastamento.
- Bloquear militar nas escalas do periodo.
- Manter contador conforme regra operacional.

## Relatorio de Escala

- Gerar relatorio por periodo, escala e militar.
- Exportar relatorio.
- Registrar geracao em auditoria.

## Auditoria

- Consultar eventos e decisoes.
- Filtrar por ator, periodo, contexto e criticidade.
- Exportar evidencias.
