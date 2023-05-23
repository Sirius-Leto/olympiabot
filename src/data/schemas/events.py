import itertools
from datetime import datetime
from typing import Optional

from pydantic import Json, validator

from .__base import BaseModel
from .__mixins import (TimestampMixin, NameDescriptionMixin, IdMixin, TagsMixin, TagsViewMixin, ReferenceMixinFactory)
from .event_types import EventTypeView, EventTypeReference
from .grades import GradeReference, GradeView
from .levels import LevelReference, LevelView
from .subjects import SubjectReference, SubjectView
import operator


class EventBase(TimestampMixin, NameDescriptionMixin, TagsMixin, BaseModel):
    begin_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    url: Optional[str] = None
    format: Optional[str]
    prizes: Optional[str]


class EventCreate(EventBase):
    event_type: EventTypeReference
    levels: list[LevelReference]
    grades: list[GradeReference]
    subjects: list[SubjectReference]


class EventView(IdMixin, TagsViewMixin, EventBase):
    event_type: Optional[EventTypeView]
    levels: Optional[list[LevelView]]
    grades: Optional[list[GradeView]]
    subjects: Optional[list[SubjectView]]

    def get_grades_display(self) -> str:
        temp = list(map(operator.attrgetter("name"), self.grades))
        # try to convert to int
        is_int = True
        for i in range(len(temp)):
            try:
                temp[i] = int(temp[i])
            except ValueError:
                is_int = False
        # if all elements are int
        if is_int:
            temp = sorted(temp)

        # convert all sequentional numbers to range: 1, 2, 3 -> 1-3
        temp = [list(group) for k, group in itertools.groupby(temp, key=lambda x, c=itertools.count(): x - next(c))]
        temp = [f"{i[0]}-{i[-1]}" if len(i) > 1 else str(i[0]) for i in temp]
        return ", ".join(temp)

    class Config:
        orm_mode = True


class EventReference(ReferenceMixinFactory(EventView)):
    ...
