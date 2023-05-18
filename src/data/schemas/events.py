from datetime import datetime
from typing import Optional

from .__base import BaseModel
from .__mixins import TimestampMixin, NameDescriptionMixin, IdMixin, TagsMixin, TagsViewMixin
from .event_types import EventTypeView


class EventBase(TimestampMixin, NameDescriptionMixin, TagsMixin, BaseModel):
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class EventCreate(EventBase):
    event_type_id: int


class EventView(IdMixin, TagsViewMixin, EventBase):
    event_type: EventTypeView

    class Config:
        orm_mode = True
