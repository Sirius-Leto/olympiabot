from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from .__base import Base
from .__mixins import IdMixin, TimestampMixin, NameDescriptionMixin, TagsMixinFactory

if TYPE_CHECKING:
    from data.models._fields import Field


class Subject(TagsMixinFactory(Base), IdMixin, TimestampMixin, NameDescriptionMixin, TagsMixinFactory(Base), Base):
    __tablename__ = "subjects"

    # field_id: Mapped[int] = mapped_column(ForeignKey("fields.id"))
    # field: Mapped['Field'] = relationship(backref="connected_subjects")
