from .__base import Base
from .__mixins import IdMixin, TimestampMixin, NameDescriptionMixin, TagsMixinFactory


class Field(IdMixin, TimestampMixin, NameDescriptionMixin, TagsMixinFactory(Base), Base):
    __tablename__ = "fields"
