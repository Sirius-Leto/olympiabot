from ._base import Base
from ._mixins import IdMixin, TimestampMixin, NameDescriptionMixin


class EventType(IdMixin, TimestampMixin, NameDescriptionMixin, Base):
    __tablename__ = "event_types"


