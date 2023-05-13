from ._base import Base
from ._mixins import IdMixin, TimestampMixin, NameDescriptionMixin


class Level(IdMixin, TimestampMixin, NameDescriptionMixin, Base):
    __tablename__ = "levels"
