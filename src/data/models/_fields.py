from ._base import Base
from ._mixins import IdMixin, TimestampMixin, NameDescriptionMixin


class Field(IdMixin, TimestampMixin, NameDescriptionMixin, Base):
    __tablename__ = "fields"
