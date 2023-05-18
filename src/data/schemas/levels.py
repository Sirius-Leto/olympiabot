from .__mixins import IdMixin, TimestampMixin, NameDescriptionMixin, TagsMixin, TagsViewMixin
from .__base import BaseModel


class FieldBase(TimestampMixin, NameDescriptionMixin, TagsMixin, BaseModel):
    ...


class FieldCreate(FieldBase):
    ...


class FieldView(IdMixin, TagsViewMixin, FieldBase):
    class Config:
        orm_mode = True
