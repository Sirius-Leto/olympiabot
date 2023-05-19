from datetime import datetime
from typing import Optional

from pydantic import Json

from .__base import BaseModel
from .__mixins import (TimestampMixin, NameDescriptionMixin, IdMixin, TagsMixin, TagsViewMixin, ReferenceMixinFactory)
from .event_types import EventTypeView, EventTypeReference
from .grades import GradeReference, GradeView
from .levels import LevelReference, LevelView
from .subjects import SubjectReference, SubjectView


class EventBase(TimestampMixin, NameDescriptionMixin, TagsMixin, BaseModel):
    begin_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    url: Optional[str] = None
    format: Json
    prizes: Json


class EventCreate(EventBase):
    event_type: EventTypeReference
    levels: list[LevelReference]
    grades: list[GradeReference]
    subjects: list[SubjectReference]


class EventView(IdMixin, TagsViewMixin, EventBase):
    event_type: EventTypeView
    levels: list[LevelView]
    grades: list[GradeView]
    subjects: list[SubjectView]

    class Config:
        orm_mode = True


class EventReference(ReferenceMixinFactory(EventView)):
    ...
