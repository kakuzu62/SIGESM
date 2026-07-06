# Coding Guidelines

## Python

- Usar Python 3.12.
- Todo codigo deve ser compativel com MyPy strict.
- Preferir dataclasses imutaveis para value objects e resultados.

## Typing

- Nao usar `Any` sem motivo claro.
- Evitar casts; quando necessarios, manter perto da fronteira tecnica.
- Retornos publicos devem ser anotados.

## Docstrings

- Classes publicas devem possuir docstring.
- Metodos publicos devem explicar contrato quando o nome nao for suficiente.

## Imports

- Imports devem apontar para camadas permitidas.
- Dominio nao importa infraestrutura, UI ou banco.
- Application nao importa presentation.

## Excecoes

- Usar a hierarquia em `core.exceptions`.
- Excecoes de dominio devem representar invariantes e regras.
- Nao usar excecao para fluxo esperado quando `Result` for mais claro.

## Logs

- Criar logger por modulo com `logging.getLogger(__name__)`.
- Logs devem registrar decisoes, falhas e tempo de execucao relevante.
- Nao registrar dados sensiveis.

## Result Pattern

- Usar `Result` para operacoes que possam falhar de forma esperada.
- Engines e policies devem retornar resultados ricos quando houver motivos,
  avisos ou metadata.

## Dependency Inversion

- Casos de uso dependem de contratos.
- Infraestrutura implementa contratos.
- DI deve ser configurada no bootstrap.

## Proibicoes

- Nao colocar logica de negocio na UI.
- Nao acessar banco diretamente fora da infraestrutura.
- Nao usar prints em codigo de producao.
- Nao criar atalhos que burlem testes, tipagem ou auditoria.
