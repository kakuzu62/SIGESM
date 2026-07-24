from __future__ import annotations

from dataclasses import dataclass

from domain.identity.entities import Role


@dataclass(frozen=True, slots=True)
class RoleListItemDTO:
    """Safe role row returned to Presentation."""

    id: str
    name: str
    normalized_name: str
    active: bool

    @classmethod
    def from_domain(cls, role: Role) -> RoleListItemDTO:
        """Create a DTO from a role entity."""
        return cls(
            id=str(role.id),
            name=role.name,
            normalized_name=role.normalized_name,
            active=role.active,
        )
