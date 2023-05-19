from .__mixins import IdMixin, TimestampMixin, NameDescriptionMixin
from .__base import Base


class Tag(IdMixin, TimestampMixin, NameDescriptionMixin, Base):
    __tablename__ = "tags"

