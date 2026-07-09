"""Repository adapters for user management."""

from presentation.modules.user_management.infrastructure.repositories.in_memory_user_management_repository import (
    InMemoryUserManagementRepository,
)

__all__ = ["InMemoryUserManagementRepository"]
