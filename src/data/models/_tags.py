from ._base import Base
from ._mixins import IdMixin, TimestampMixin, NameDescriptionMixin


class Tag(IdMixin, TimestampMixin, NameDescriptionMixin, Base):
    __tablename__ = "tags"
