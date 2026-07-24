# STS-001F TECH - Atribuicao de Perfis aos Usuarios

## Fluxo

```text
UserListView
  -> UserRolesDialog
  -> UserRolesViewModel
  -> AssignUserRolesService
  -> AssignUserRolesCommand
  -> AssignUserRolesHandler
  -> IUserRepository
  -> IRoleRepository
  -> UserRolesUnitOfWork
  -> Persistence
```

## Modelo

`Role` foi consolidado com:

- `normalized_name`;
- `active`;
- `created_at`;
- `updated_at`.

O relacionamento muitos-para-muitos `identity_user_roles` existente foi
reutilizado.

## Application

Foram adicionados:

- `AssignUserRolesCommand`;
- `AssignUserRolesCommandValidator`;
- `AssignUserRolesHandler`;
- `AssignUserRolesResultDTO`;
- `AssignUserRolesService`;
- `ListAvailableRolesQuery`;
- `ListAvailableRolesHandler`;
- `RoleListItemDTO`;
- `UserRolesUnitOfWork`.

## Protecao Administrativa

A protecao do ultimo administrador ativo usa:

- `Role.normalized_name == "ADMINISTRADOR"`;
- usuario ativo;
- contagem de usuarios ativos com o perfil.

Nao usa username, e-mail, nome de botao ou heuristica de interface.

## Persistencia

A migration baseline `20260723_0000_create_identity_schema` cria o schema
Identity em banco vazio, preservando a cadeia Alembic para instalacoes novas.

A migration `20260723_0002_add_identity_role_assignment_fields` adiciona
`normalized_name` e `active` em `identity_roles`.

## Debitos

- autorizacao granular pendente para STS-001G;
- controle otimista ausente;
- execucao sincronona na UI;
- invalidacao de sessoes apos reset de senha.
