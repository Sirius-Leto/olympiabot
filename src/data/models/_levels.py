from .__base import Base
from .__mixins import IdMixin, TimestampMixin, NameDescriptionMixin, TagsMixinFactory


class Level(IdMixin, TimestampMixin, NameDescriptionMixin, TagsMixinFactory(Base), Base):
    __tablename__ = "levels"
