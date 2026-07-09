from __future__ import annotations

from domain.identity.entities import Role, User
from presentation.modules.user_management.application.dto import (
    RoleDTO,
    UserDTO,
    UserDetailsDTO,
    UserListItemDTO,
)


class UserMapper:
    """Maps identity domain objects to user management DTOs."""

    @staticmethod
    def role_to_dto(role: Role) -> RoleDTO:
        """Map a role entity to a DTO."""
        return RoleDTO(id=str(role.id), name=role.name, description=role.description)

    @classmethod
    def to_dto(cls, user: User) -> UserDTO:
        """Map a user aggregate to a DTO."""
        return UserDTO(
            id=str(user.id),
            username=user.username.value,
            email=user.email.value,
            active=user.active,
            roles=tuple(cls.role_to_dto(role) for role in user.roles),
            created_at=user.created_at,
            updated_at=user.updated_at,
        )

    @classmethod
    def to_details(cls, user: User) -> UserDetailsDTO:
        """Map a user aggregate to a detailed DTO."""
        dto = cls.to_dto(user)
        return UserDetailsDTO(
            id=dto.id,
            username=dto.username,
            email=dto.email,
            active=dto.active,
            roles=dto.roles,
            created_at=dto.created_at,
            updated_at=dto.updated_at,
        )

    @staticmethod
    def to_list_item(user: User) -> UserListItemDTO:
        """Map a user aggregate to a table item."""
        return UserListItemDTO(
            id=str(user.id),
            username=user.username.value,
            email=user.email.value,
            active=user.active,
            roles=tuple(role.name for role in user.roles),
            updated_at=user.updated_at,
        )
