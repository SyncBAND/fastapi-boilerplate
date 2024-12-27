from datetime import datetime
from uuid import uuid4

from sqlalchemy import func, UUID
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.types import TIMESTAMP


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True
    __mapper_args__ = {"eager_defaults": True}

    id: Mapped[UUID] = mapped_column(
        UUID,
        default=uuid4,
        primary_key=True,
        sort_order=-3
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=func.now(),
        nullable=False,
        sort_order=-2
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=func.now(),
        nullable=False,
        onupdate=func.now(),
        sort_order=-1
    )
