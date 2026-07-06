# Contribuindo com o SIGESM Enterprise

## Fluxo de Trabalho

1. Crie uma branch a partir de `main`.
2. Mantenha mudancas pequenas, revisaveis e alinhadas a Clean Architecture.
3. Atualize testes e documentacao quando alterar comportamento ou contrato.
4. Abra pull request descrevendo motivacao, mudancas e validacoes executadas.

## Padroes Obrigatorios

- Python 3.12.
- Typing completo e compativel com MyPy strict.
- Black e Ruff sem violacoes.
- Testes automatizados para regras de dominio, policies, engines e adapters.
- Dominio sem dependencia de infraestrutura, banco ou interface.
- Infraestrutura sem regra de negocio.
- Presentation sem acesso direto ao banco.

## Validacao Local

```powershell
.\.venv\Scripts\python.exe -m black --check src tests migrations
.\.venv\Scripts\python.exe -m ruff check src tests migrations
.\.venv\Scripts\python.exe -m mypy src tests migrations
.\.venv\Scripts\python.exe -m pytest
```

## Documentacao

Atualize `README.md`, `ARCHITECTURE.md`, `docs/CHANGELOG.md` e ADRs quando uma
mudanca afetar arquitetura, padroes ou operacao.
