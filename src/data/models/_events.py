from datetime import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .__base import Base
from .__mixins import IdMixin, TimestampMixin, NameDescriptionMixin, TagsMixinFactory

if TYPE_CHECKING:
    from data.models._event_types import EventType
    # from data.models._levels import Level


class Event(IdMixin, TimestampMixin, NameDescriptionMixin, TagsMixinFactory(Base), Base):
    __tablename__ = "events"

    start_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    end_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    event_type_id: Mapped[int] = mapped_column(ForeignKey('event_types.id'))
    event_type: Mapped['EventType'] = relationship(backref="connected_events")
    # levels: Mapped[List['Level']] = relationship("Level", secondary="events_x_levels")
