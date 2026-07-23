# TEST-001 - Plano de Testes da STS-001A

## Testes Unitarios

- `ListUsersHandler` retorna pagina.
- `ListUsersHandler` rejeita pagina igual a zero.
- `ListUsersHandler` rejeita tamanho de pagina invalido.
- `ListUsersHandler` rejeita campo de ordenacao invalido.
- `ListUsersHandler` aplica pesquisa.
- `ListUsersHandler` retorna resultado vazio para pesquisa sem correspondencia.
- `ListUsersHandler` retorna ultima pagina parcial.
- `ListUsersHandler` aplica ordenacao.
- `UserListViewModel` carrega usuarios.
- `UserListViewModel` pesquisa usuarios.
- `UserListViewModel` alterna ordenacao ASC/DESC.
- `UserListViewModel` publica propriedades de paginacao.
- `UserListViewModel` atualiza `error_message` em falha.
- `UserListViewModel` preserva dados carregados quando uma consulta falha.
- `UserListViewModel` publica `is_loading`.
- `UserListViewModel` emite sinal para novo usuario.
- `UserListViewModel` emite sinal para edicao.
- `UserListViewModel` ignora edicao sem selecao.
- `UserTableModel` exibe dados.
- `UserTableModel` trata tabela vazia.
- `UserListItemDTO` nao expoe senha, hash ou token.

## Politica de Falha

Quando uma consulta falha, a ViewModel preserva explicitamente os dados
anteriores e atualiza `error_message`. A tabela somente e substituida quando a
Application retorna uma pagina valida.

## Dados de Teste

Testes de listagem nao executam algoritmo real de hash de senha. A suite usa um
hash Argon2id fixo valido para satisfazer os invariantes do dominio sem testar
criptografia fora do escopo.

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
