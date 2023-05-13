from datetime import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ._base import Base
from ._mixins import IdMixin, TimestampMixin, NameDescriptionMixin

if TYPE_CHECKING:
    from data.models._event_types import EventType
    # from data.models._levels import Level


class Event(IdMixin, TimestampMixin, NameDescriptionMixin, Base):
    __tablename__ = "events"

    start_date: Mapped[datetime] = mapped_column(DateTime)
    end_date: Mapped[datetime] = mapped_column(DateTime)

    event_type_id: Mapped[int] = mapped_column(ForeignKey('event_types.id'))
    event_type: Mapped['EventType'] = relationship(backref="connected_events")
    # levels: Mapped[List['Level']] = relationship("Level", secondary="events_x_levels")
