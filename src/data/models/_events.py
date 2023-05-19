from datetime import date
from typing import TYPE_CHECKING, List, Dict, Any

from sqlalchemy import DateTime, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .__base import Base
from .__mixins import IdMixin, TimestampMixin, NameDescriptionMixin, TagsMixinFactory

if TYPE_CHECKING:
    from ._event_types import EventType
    from ._levels import Level
    from ._subjects import Subject
    from ._grades import Grade


class Event(IdMixin, TimestampMixin, NameDescriptionMixin, TagsMixinFactory(Base), Base):
    __tablename__ = "events"

    begin_date: Mapped[date] = mapped_column(DateTime, nullable=True)
    end_date: Mapped[date] = mapped_column(DateTime, nullable=True)
    url: Mapped[str] = mapped_column(nullable=True, default="")
    format: Mapped[Dict[str, Any]] = mapped_column(nullable=True, default="{}")
    prizes: Mapped[Dict[str, Any]] = mapped_column(nullable=True, default="{}")

    event_type_id: Mapped[int] = mapped_column(ForeignKey('event_types.id'))
    event_type: Mapped['EventType'] = relationship(backref="connected_events")
    levels: Mapped[List['Level']] = relationship("Level",
                                                 secondary="events_x_levels",
                                                 backref="connected_events")
    grades: Mapped[List['Grade']] = relationship("Grade",
                                                 secondary="events_x_grades",
                                                 backref="connected_events")
    subjects: Mapped[List['Subject']] = relationship("Subject",
                                                     secondary="events_x_subjects",
                                                     backref="connected_events")


event_x_subjects = Table(
    "events_x_subjects",
    Base.metadata,
    Column("event_id", ForeignKey("events.id"), primary_key=True),
    Column("subject_id", ForeignKey("subjects.id"), primary_key=True),
)

event_x_levels = Table(
    "events_x_levels",
    Base.metadata,
    Column("event_id", ForeignKey("events.id"), primary_key=True),
    Column("level_id", ForeignKey("levels.id"), primary_key=True),
)

event_x_grades = Table(
    "events_x_grades",
    Base.metadata,
    Column("event_id", ForeignKey("events.id"), primary_key=True),
    Column("grade_id", ForeignKey("grades.id"), primary_key=True),
)
