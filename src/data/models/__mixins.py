from datetime import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import DateTime, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, declared_attr, relationship, DeclarativeBase
from sqlalchemy.sql import func

if TYPE_CHECKING:
    from ._tags import Tag


class IdMixin:
    id: Mapped[int] = mapped_column(primary_key=True)


class NameDescriptionMixin:
    name: Mapped[str] = mapped_column(nullable=False, )
    description: Mapped[str] = mapped_column(nullable=True, default="")

    @declared_attr
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self.name}>"


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


def TagsMixinFactory(
        CurrentBase: type[DeclarativeBase],
) -> type:
    class TagsMixin:
        __tablename__: str

        # create a table for many-to-many relationship
        @declared_attr
        def tags(self) -> Mapped[List['Tag']]:
            Table(
                f"{self.__tablename__}_x_tags",
                CurrentBase.metadata,
                Column("tag_id", ForeignKey("tags.id"), primary_key=True),
                Column(f"{self.__tablename__}_id", ForeignKey(f"{self.__tablename__}.id"), primary_key=True),
            )

            return relationship("Tag", secondary=f"{self.__tablename__}_x_tags")

    return TagsMixin


__all__ = [
    "IdMixin",
    "NameDescriptionMixin",
    "TimestampMixin",
    "TagsMixinFactory",
]
