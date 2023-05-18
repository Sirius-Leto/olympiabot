from .__base import BaseModel
from .__mixins import IdMixin, TimestampMixin, NameDescriptionMixin, TagsMixin, TagsViewMixin


class FieldBase(TimestampMixin, NameDescriptionMixin, TagsMixin, BaseModel):
    ...


class FieldCreate(FieldBase):
    ...


class FieldView(IdMixin, TagsViewMixin, FieldBase):
    class Config:
        orm_mode = True


class FieldReference(IdMixin, BaseModel):
    ...
