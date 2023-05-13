from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from ._base import Base
from ._mixins import IdMixin, TimestampMixin, NameDescriptionMixin

if TYPE_CHECKING:
    from data.models._fields import Field


class Subject(IdMixin, TimestampMixin, NameDescriptionMixin, Base):
    __tablename__ = "subjects"

    field_id: Mapped[int] = mapped_column(ForeignKey("fields.id"))
    field: Mapped['Field'] = relationship(backref="connected_subjects")
