from enum import Enum

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base
from src.core.security.access_control import Allow, Everyone, RolePrincipal, UserPrincipal


class UserPermission(Enum):
    CREATE = "create"
    READ = "read"
    EDIT = "edit"
    DELETE = "delete"


class User(Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    firstname: Mapped[str] = mapped_column(String(255), nullable=False)
    lastname: Mapped[str] = mapped_column(String(255), nullable=False)
    is_admin: Mapped[bool] = mapped_column(default=False)

    moods = relationship(
        "Mood", back_populates="user", lazy="raise", passive_deletes=True
    )

    def __acl__(self):
        basic_permissions = [UserPermission.READ, UserPermission.CREATE]
        self_permissions = [
            UserPermission.READ,
            UserPermission.EDIT,
            UserPermission.CREATE,
        ]
        all_permissions = list(UserPermission)

        return [
            (Allow, Everyone, basic_permissions),
            (Allow, UserPrincipal(value=self.id), self_permissions),
            (Allow, RolePrincipal(value="admin"), all_permissions),
        ]
