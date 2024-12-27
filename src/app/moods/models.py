# pylint: disable=unsubscriptable-object
from enum import Enum

from sqlalchemy import ForeignKey, Integer, Text, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base
from src.core.security.access_control import (
    Allow,
    Authenticated,
    RolePrincipal,
    UserPrincipal,
)


class MoodPermission(Enum):
    CREATE = "create"
    READ = "read"
    EDIT = "edit"
    DELETE = "delete"


class Mood(Base):
    __tablename__ = "moods"

    learning: Mapped[Text] = mapped_column(Text, nullable=False)
    personal_note: Mapped[Text] = mapped_column(Text, nullable=False)
    rating: Mapped[Integer] = mapped_column(Integer, nullable=False)

    user_id: Mapped[UUID] = mapped_column(
        UUID, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    user: Mapped["User"] = relationship(
        "User", back_populates="moods", uselist=False, lazy="raise"
    )

    def __acl__(self):
        basic_permissions = [MoodPermission.CREATE]
        self_permissions = [
            MoodPermission.READ,
            MoodPermission.EDIT,
            MoodPermission.DELETE,
        ]
        all_permissions = list(MoodPermission)

        return [
            (Allow, Authenticated, basic_permissions),
            (Allow, UserPrincipal(self.user_id), self_permissions),
            (Allow, RolePrincipal("admin"), all_permissions),
        ]
