from .__base import BaseModel
from .__mixins import IdMixin, TimestampMixin, NameDescriptionMixin, TagsViewMixin


class EventTypeBase(TimestampMixin, NameDescriptionMixin, BaseModel):
    ...


class EventTypeCreate(EventTypeBase):
    ...


class EventTypeView(IdMixin, TagsViewMixin, EventTypeBase):
    class Config:
        orm_mode = True
