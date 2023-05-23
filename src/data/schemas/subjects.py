from .__base import BaseModel
from .__mixins import IdMixin, TimestampMixin, NameDescriptionMixin, TagsMixin, TagsViewMixin


# from .fields import FieldReference, FieldView


class SubjectBase(TimestampMixin, NameDescriptionMixin, TagsMixin, BaseModel):
    ...


class SubjectCreate(SubjectBase):
    # fields: list[FieldReference]
    ...


class SubjectView(IdMixin, TagsViewMixin, SubjectBase):
    # fields: list[FieldView]

    class Config:
        orm_mode = True


class SubjectReference(IdMixin, BaseModel):
    ...
