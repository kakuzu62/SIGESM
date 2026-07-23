# TEST-002 - Plano de Testes da STS-001B

## Testes Criados

Arquivo:

```text
tests/unit/presentation/modules/test_user_creation.py
```

Cobertura:

- estado inicial do usuario criado;
- validacao de campos obrigatorios;
- validacao de limites;
- normalizacao de dados de entrada;
- criacao com commit;
- login duplicado com rollback;
- e-mail duplicado com rollback;
- conflito de unicidade no commit;
- username, e-mail e senha invalidos;
- confirmacao de senha divergente;
- sucesso emitido por sinal;
- limpeza de senhas apos sucesso;
- bloqueio de duplo envio durante loading;
- botao Salvar conforme validade;
- erro mantendo dialogo aberto;
- usuario criado aparecendo na listagem;
- persistencia SQLAlchemy com SQLite.

## Quality Gate

Comandos obrigatorios:

```powershell
.\.venv\Scripts\python.exe -m black src tests migrations build
.\.venv\Scripts\python.exe -m ruff check src tests migrations build --fix
.\.venv\Scripts\python.exe -m mypy src tests migrations
.\.venv\Scripts\python.exe -m pytest
```

Resultado esperado: todos aprovados antes da AR-002.

