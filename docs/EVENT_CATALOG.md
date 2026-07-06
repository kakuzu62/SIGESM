# Event Catalog

Catalogo oficial de eventos de dominio existentes e previstos.

| Evento | Contexto | Origem | Payload conceitual | Consumidores previstos | Impacto | Criticidade |
|---|---|---|---|---|---|---|
| OrganizationCreated | Organization | Organization.register/create | organization_id, code, name, created_at | Audit, Reports | Registra nova organizacao | Media |
| MilitaryRegistered | Military | MilitaryPerson.register | military_id, cpf, rank, status, created_at | Audit, ServiceScale, Reports | Habilita militar no sistema | Alta |
| ServiceAssignmentCreated | ServiceScale | ServiceScale.assign | assignment_id, military_id, date, scale_type, role_id | Audit, Notification, Reports | Cria designacao de servico | Alta |
| ServiceAssignmentCancelled | ServiceScale | ServiceScale.cancel | assignment_id, reason, cancelled_at | Audit, Notification, Reports | Cancela designacao | Alta |
| MilitaryDeclaredEligible | ServiceScale | EligibilityEngine.evaluate | military_id, service_date, scale_type, metadata | Audit, Generation | Registra decisao positiva | Media |
| MilitaryDeclaredIneligible | ServiceScale | EligibilityEngine.evaluate | military_id, service_date, reasons, metadata | Audit, Generation | Bloqueia selecao automatica | Alta |
| ScaleGenerated | ServiceScale | ScaleGenerationEngine.generate | generation_id, date, scale_type, selected, statistics | Audit, Reports | Consolida escala gerada | Alta |
| MilitarySelected | ServiceScale | GenerationPolicy | generation_id, military_id, reason, score | Audit, Notification | Informa selecao automatica | Alta |
| MilitarySkipped | ServiceScale | GenerationPolicy | generation_id, military_id, reasons | Audit | Explica descarte | Alta |
| OfficialSwapApproved | ServiceExchange | OfficialSwapPolicy | swap_id, participants, approved_by, approved_at | Audit, Reports | Autoriza troca real | Alta |
| OfficialSwapRejected | ServiceExchange | OfficialSwapPolicy | swap_id, reasons, rejected_at | Audit, Notification | Rejeita troca | Alta |
| ServiceSaleApproved | ServiceExchange | ServiceSalePolicy | sale_id, seller, buyer, service_date, approved_at | Audit, Reports | Autoriza venda de servico | Alta |
| ServiceSaleRejected | ServiceExchange | ServiceSalePolicy | sale_id, reasons, rejected_at | Audit, Notification | Rejeita venda | Alta |
| UserCreated | Identity | User use case | user_id, username, profiles | Audit | Habilita acesso | Alta |
| UserLocked | Identity | Security policy | user_id, reason, locked_at | Audit, Notification | Bloqueia acesso | Critica |
| LeaveApproved | Leave | Leave policy | leave_id, military_id, period, reason | Audit, ServiceScale | Torna militar indisponivel | Alta |
| AutomaticDecisionRecorded | Audit | Audit service | decision_id, source, metadata | Reports | Preserva rastreabilidade | Critica |
| NotificationDelivered | Notification | Notification service | notification_id, recipient, channel | Audit | Confirma comunicacao | Baixa |
| ReportGenerated | Reports | Report use case | report_id, format, filters | Audit | Gera evidencias operacionais | Media |
| SettingChanged | Settings | Settings use case | key, old_value, new_value, actor | Audit | Altera regra parametrica | Alta |
