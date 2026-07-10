# TEST-001 - Plano de Testes da STS-001A

## Testes Unitarios

- `ListUsersHandler` retorna pagina.
- `ListUsersHandler` aplica pesquisa.
- `ListUsersHandler` aplica ordenacao.
- `UserListViewModel` carrega usuarios.
- `UserListViewModel` pesquisa usuarios.
- `UserTableModel` exibe dados.

## Testes Automatizados

Arquivo:

```text
tests/unit/presentation/modules/test_user_listing.py
```

## Quality Gate

Comandos obrigatorios:

```powershell
.\.venv\Scripts\python.exe -m black src tests migrations build
.\.venv\Scripts\python.exe -m ruff check src tests migrations build --fix
.\.venv\Scripts\python.exe -m mypy src tests migrations
.\.venv\Scripts\python.exe -m pytest
```

## Resultado Esperado

Todos os comandos devem finalizar sem erros antes da Architecture Review.
