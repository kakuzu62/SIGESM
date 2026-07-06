# ADR-0002: Bounded Contexts para dominio militar

## Status

Aceita.

## Contexto

O sistema cobre organizacao militar, militares, escalas, trocas, vendas de
servico e futuros modulos operacionais. Um dominio unico ficaria grande demais.

## Decisao

Organizar `src/domain` por bounded contexts. Cada contexto possui entidades,
value objects, eventos, repositories, specifications, policies, engines e
excecoes proprias quando necessario.

## Consequencias

- Modulos evoluem com menor acoplamento.
- Linguagem ubqua fica localizada por area de negocio.
- Integrações entre contextos devem ocorrer por contratos ou eventos, nao por
  acesso direto a detalhes internos.
