# Event Storming

Mapa inicial de eventos, comandos, agregados e policies do SIGESM Enterprise.

## Identity

- Comandos: CreateUser, AuthenticateUser, LockUser, ChangePassword.
- Agregados: User, Profile.
- Eventos: UserCreated, UserAuthenticated, UserLocked, PasswordChanged.
- Policies: PasswordPolicy, LoginAttemptPolicy, PermissionPolicy.

## Organization

- Comandos: RegisterOrganization, UpdateOrganization, ChangeOrganizationSetting.
- Agregados: Organization.
- Eventos: OrganizationCreated, OrganizationUpdated, OrganizationSettingChanged.
- Policies: UniqueOrganizationCodePolicy.

## Military

- Comandos: RegisterMilitary, ActivateMilitary, DeactivateMilitary, ChangeRank,
  UpdateContact.
- Agregados: MilitaryPerson.
- Eventos: MilitaryRegistered, MilitaryActivated, MilitaryDeactivated,
  MilitaryRankChanged, MilitaryContactUpdated.
- Policies: CPFValidationPolicy, MilitaryStatusPolicy.

## ServiceScale

- Comandos: CreateScale, AddServiceRole, AssignMilitary, CancelAssignment,
  CompleteAssignment, GenerateScale.
- Agregados: ServiceScale.
- Eventos: ServiceAssignmentCreated, ServiceAssignmentCancelled,
  ServiceAssignmentCompleted, ScaleGenerated, MilitarySelected, MilitarySkipped,
  MilitaryDeclaredEligible, MilitaryDeclaredIneligible.
- Policies: MinimumRestPolicy, EligibilityPolicy, GenerationPolicy,
  FairnessPolicy, TieBreakPolicy.

## ServiceExchange

- Comandos: RequestOfficialSwap, ApproveOfficialSwap, RejectOfficialSwap,
  RequestServiceSale, ApproveServiceSale, RejectServiceSale.
- Agregados: OfficialSwap, ServiceSale.
- Eventos: OfficialSwapApproved, OfficialSwapRejected, ServiceSaleApproved,
  ServiceSaleRejected.
- Policies: OfficialSwapPolicy, ServiceSalePolicy.

## Leave

- Comandos: RegisterLeave, ApproveLeave, RejectLeave, CancelLeave.
- Agregados: LeaveRecord.
- Eventos: LeaveRegistered, LeaveApproved, LeaveRejected, LeaveCancelled.
- Policies: LeaveConflictPolicy, LeaveEligibilityPolicy.

## Audit

- Comandos: RecordAuditEntry, RecordAutomaticDecision.
- Agregados: AuditEntry, DecisionRecord.
- Eventos: AuditEntryRecorded, AutomaticDecisionRecorded.
- Policies: AuditRetentionPolicy.

## Fluxo Principal de Geracao de Escala

1. GenerateScale solicitado.
2. ScaleGenerationEngine carrega candidatos.
3. EligibilityEngine avalia cada militar.
4. Eventos MilitaryDeclaredEligible ou MilitaryDeclaredIneligible sao gerados.
5. GenerationPolicy aplica fairness e desempate.
6. MilitarySelected e MilitarySkipped sao registrados.
7. ScaleGenerated consolida a execucao.
8. Audit registra a decisao automatica.

## Fluxo Principal de Troca Oficial

1. RequestOfficialSwap solicitado.
2. SwapValidationEngine avalia os dois militares nos novos dias.
3. OfficialSwapPolicy decide aprovacao ou rejeicao.
4. Evento OfficialSwapApproved ou OfficialSwapRejected e emitido.
5. Audit registra decisao, motivos e autorizador.

## Fluxo Principal de Venda de Servico

1. RequestServiceSale solicitado.
2. ServiceSaleEngine avalia comprador e servico extraordinario.
3. ServiceSalePolicy preserva contador base do comprador.
4. Evento ServiceSaleApproved ou ServiceSaleRejected e emitido.
5. Audit registra decisao e impacto operacional.

## Riscos e Decisoes Pendentes

- Definir granularidade final dos eventos persistidos.
- Separar eventos de dominio de eventos de integracao quando houver API.
- Definir outbox transacional antes de qualquer publicacao assíncrona.
- Definir consumidores obrigatorios de auditoria para eventos criticos.
