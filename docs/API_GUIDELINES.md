# API Guidelines

Mesmo sendo desktop, o SIGESM deve estar preparado para uma futura API com
FastAPI.

## FastAPI

- API futura deve viver fora do dominio.
- Endpoints devem chamar use cases da application layer.
- Nenhum endpoint deve acessar repository concreto diretamente.

## DTOs

- DTOs de entrada e saida devem ser explicitos.
- DTOs nao devem vazar entidades de dominio.
- Validacoes estruturais ficam no DTO; regras de negocio ficam no dominio.

## Versionamento

- Rotas publicas devem iniciar com `/api/v1`.
- Mudancas incompatveis devem abrir nova versao.

## Autenticacao

- Usar tokens ou sessao conforme decisao futura.
- Permissoes devem ser avaliadas por policy central.

## Erros

- Erros devem retornar codigo, mensagem e detalhes seguros.
- Excecoes internas nao devem vazar stack trace.

## Paginacao e Filtros

- Listagens devem suportar pagina, tamanho, ordenacao e filtros.
- Limites maximos devem proteger performance.

## Contratos

- OpenAPI deve ser gerado e revisado.
- Contratos devem ser estaveis e cobertos por testes.
