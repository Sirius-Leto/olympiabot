from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column, declared_attr


class IdMixin:
    id: Mapped[int] = mapped_column(primary_key=True)


class NameDescriptionMixin:
    name: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()

    @declared_attr
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self.name}>"


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow
    )
