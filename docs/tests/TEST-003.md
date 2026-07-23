# TEST-003 - Plano de Testes da STS-001C

## Testes Criados

Arquivo:

```text
tests/unit/presentation/modules/test_user_editing.py
```

Cobertura:

- atualizacao valida no agregado;
- preservacao de ID, senha, status, roles e `created_at`;
- validacao de ID, nome, login, e-mail e limite maximo;
- normalizacao de dados;
- update com commit;
- usuario inexistente com rollback;
- login duplicado;
- e-mail duplicado;
- proprio login/e-mail permitidos;
- conflito de unicidade no commit;
- DTO sem senha/hash;
- `EditUserViewModel` com `has_changes`, `can_submit`, `is_loading` e sinais;
- dialogo em modo edicao sem campos de senha;
- persistencia SQLite via SQLAlchemy;
- rollback preservando dados originais.

## Quality Gate

Comandos obrigatorios:

```powershell
.\.venv\Scripts\python.exe -m black src tests migrations build
.\.venv\Scripts\python.exe -m ruff check src tests migrations build --fix
.\.venv\Scripts\python.exe -m mypy src tests migrations
.\.venv\Scripts\python.exe -m pytest
```

Resultado esperado: todos aprovados antes da AR-003.

