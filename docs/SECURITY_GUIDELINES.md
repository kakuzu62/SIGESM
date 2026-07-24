# Security Guidelines

## Senhas

- Senhas devem ser armazenadas somente com hash forte e salt.
- Politica minima: tamanho, complexidade e bloqueio de senhas comuns.
- Redefinicao de senha deve ser auditada.

## Sessao

- Sessoes devem expirar por inatividade.
- Logout deve invalidar a sessao.
- Tentativas simultaneas suspeitas devem ser registradas.
- Usuario inativo nao deve autenticar, mesmo com credenciais validas.
- A interface de login deve manter mensagens seguras e evitar revelar detalhes
  excessivos sobre o estado da conta.

## Bloqueio por Tentativas

- Acesso deve ser bloqueado apos limite configuravel de falhas.
- Desbloqueio deve exigir permissao adequada ou politica definida.

## Auditoria

- Login, logout, falhas, mudancas de permissao e decisoes automaticas devem ser
  auditados.
- Auditoria deve evitar expor segredos.

## Dados Sensiveis

- CPF, telefone e dados pessoais devem ser exibidos somente quando necessario.
- Logs nao devem conter senha, token ou segredo.
- Backups devem ser protegidos.

## Permissoes

- Aplicar principio do menor privilegio.
- Perfis devem agrupar permissoes por responsabilidade.
- Operacoes criticas exigem permissao explicita.
