"""Persistence adapters for user management."""

from presentation.modules.user_management.infrastructure.persistence.sqlalchemy_user_creation_unit_of_work import (
    SqlAlchemyUserCreationUnitOfWork,
    SqlAlchemyUserCreationUnitOfWorkFactory,
)
from presentation.modules.user_management.infrastructure.persistence.sqlalchemy_reset_password_unit_of_work import (
    SqlAlchemyResetPasswordUnitOfWork,
    SqlAlchemyResetPasswordUnitOfWorkFactory,
)
from presentation.modules.user_management.infrastructure.persistence.sqlalchemy_user_status_unit_of_work import (
    SqlAlchemyUserStatusUnitOfWork,
    SqlAlchemyUserStatusUnitOfWorkFactory,
)
from presentation.modules.user_management.infrastructure.persistence.sqlalchemy_user_update_unit_of_work import (
    SqlAlchemyUserUpdateUnitOfWork,
    SqlAlchemyUserUpdateUnitOfWorkFactory,
)

__all__ = [
    "SqlAlchemyUserCreationUnitOfWork",
    "SqlAlchemyUserCreationUnitOfWorkFactory",
    "SqlAlchemyResetPasswordUnitOfWork",
    "SqlAlchemyResetPasswordUnitOfWorkFactory",
    "SqlAlchemyUserStatusUnitOfWork",
    "SqlAlchemyUserStatusUnitOfWorkFactory",
    "SqlAlchemyUserUpdateUnitOfWork",
    "SqlAlchemyUserUpdateUnitOfWorkFactory",
]
