# Data Architecture

Este documento define a arquitetura de dados planejada para o SIGESM Enterprise
antes da implementacao funcional da Release 1.0. Nenhuma tabela ou migration e
criada nesta release.

## Objetivos

- Definir um modelo conceitual completo por bounded context.
- Preparar um modelo logico evolutivo, compativel com DDD e Clean Architecture.
- Orientar um modelo fisico compativel com SQLite e PostgreSQL.
- Definir convencoes de migrations, auditoria, historico e regras automaticas.
- Registrar riscos tecnicos e decisoes pendentes.

## Modelo Conceitual

O SIGESM organiza seus dados por contextos de negocio:

- Identity: usuarios, perfis, permissoes e sessoes.
- Organization: organizacoes militares e parametros institucionais.
- Military: cadastro, status, posto, graduacao e contatos de militares.
- ServiceScale: escalas, funcoes, designacoes, elegibilidade e geracao.
- ServiceExchange: troca oficial e venda de servico.
- Leave: afastamentos, licencas, dispensas e indisponibilidades.
- Audit: eventos, decisoes automaticas e trilhas de alteracao.
- Notification: mensagens internas e avisos operacionais.
- Reports: consultas materializadas e historico de geracao.
- Settings: parametros configuraveis de unidade, escala e seguranca.

## Modelo Logico por Bounded Context

### Identity

- `users`: credenciais, status, bloqueio e ultimo acesso.
- `profiles`: agrupamento de permissoes.
- `permissions`: acoes autorizaveis.
- `user_profiles`: associacao entre usuarios e perfis.
- `profile_permissions`: associacao entre perfis e permissoes.
- `sessions`: sessoes ativas e expiradas.

### Organization

- `organizations`: organizacao militar, codigo, nome, localidade e status.
- `organization_settings`: parametros especificos de uma organizacao.

### Military

- `military_persons`: identidade militar, CPF, nome, posto, telefone e status.
- `military_rank_history`: historico de posto ou graduacao.
- `military_contact_history`: historico de contato quando exigido.
- `military_restrictions`: restricoes individuais operacionais.

### ServiceScale

- `service_scales`: escala por tipo, data base, organizacao e situacao.
- `service_roles`: funcoes de servico disponiveis por escala.
- `service_assignments`: designacoes de militares para servico.
- `service_assignment_history`: alteracoes de designacao.
- `scale_generation_runs`: execucoes do motor de geracao.
- `scale_generation_candidates`: candidatos analisados e motivos de descarte.

### ServiceExchange

- `official_swaps`: trocas oficiais entre militares.
- `service_sales`: vendas/passagens de servico.
- `exchange_decisions`: decisoes de aprovacao, rejeicao e motivos.

### Leave

- `leave_records`: afastamentos, licencas e periodos de indisponibilidade.
- `leave_documents`: metadados de documentos comprobatórios, sem armazenar
  arquivos sensiveis diretamente no banco inicial.

### Audit

- `audit_entries`: acoes de usuario e eventos de sistema.
- `decision_records`: decisoes automaticas, regras avaliadas e metadata.
- `domain_event_outbox`: eventos de dominio pendentes de publicacao futura.

### Notification

- `notifications`: mensagens geradas.
- `notification_recipients`: destinatarios, status e tentativa de entrega.

### Reports

- `report_definitions`: relatorios configurados.
- `report_runs`: execucoes, filtros e formato de saida.

### Settings

- `settings`: parametros globais e por escopo.
- `setting_history`: historico de alteracoes.

## Modelo Fisico

### Compatibilidade SQLite e PostgreSQL

- Usar tipos SQLAlchemy portaveis sempre que possivel.
- UUID deve ser armazenado como texto canonico em SQLite e pode migrar para UUID
  nativo em PostgreSQL se o adapter permitir.
- Datas e horas devem ser timezone-aware na aplicacao e persistidas em formato
  consistente.
- Booleanos devem usar tipo abstrato do SQLAlchemy.
- JSON deve ser planejado com fallback textual para SQLite quando necessario.

### Chaves

- Chave primaria padrao: `id`.
- Identificadores externos de dominio devem possuir constraints unicas.
- Tabelas associativas devem possuir chave primaria propria quando precisarem de
  auditoria, timestamps ou metadata.

### Integridade

- Foreign keys devem ser explicitas.
- Cascatas devem ser conservadoras.
- Exclusoes fisicas devem ser evitadas em dados operacionais.

## Migrations Alembic

- Toda tabela deve nascer por migration versionada.
- Migrations devem ser pequenas, revisaveis e nomeadas por intencao.
- Alteracoes destrutivas devem ter plano de migracao e backup.
- Dados iniciais devem ser separados de alteracoes estruturais quando possivel.
- Nao usar migrations para executar regra de negocio.

## Auditoria, Timestamps e Historico

- Tabelas operacionais devem possuir `created_at` e `updated_at`.
- Quando houver desativacao logica, usar `deleted_at` e `deleted_by`.
- Alteracoes sensiveis devem gerar entrada em `audit_entries`.
- Decisoes automaticas devem gerar `decision_records`.
- Historico deve ser usado quando a mudanca passada tiver valor operacional ou
  juridico.

## Soft Delete

Usar soft delete para:

- usuarios;
- militares;
- organizacoes;
- funcoes de servico;
- parametros;
- registros operacionais que afetem auditoria.

Evitar soft delete para:

- tabelas temporarias;
- registros tecnicos recriaveis;
- associacoes sem valor historico.

## Riscos Tecnicos

- Divergencia entre recursos SQLite e PostgreSQL.
- Crescimento de tabelas de auditoria e decisoes automaticas.
- Consultas pesadas de relatorios sobre dados operacionais.
- Excesso de JSON dificultando integridade relacional.
- Historico duplicado entre audit trail e tabelas especificas de historico.

## Decisoes Pendentes

- Definir estrategia final de UUID para PostgreSQL.
- Definir politica de retencao de auditoria.
- Definir se relatorios usarao tabelas materializadas.
- Definir criptografia local de dados sensiveis.
- Definir modelo definitivo de backup e restauracao.
