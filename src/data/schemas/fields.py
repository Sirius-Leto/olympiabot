from .__mixins import IdMixin, TimestampMixin, NameDescriptionMixin, TagsMixin, TagsViewMixin, ReferenceMixinFactory
from .__base import BaseModel


class FieldBase(TimestampMixin, NameDescriptionMixin, TagsMixin, BaseModel):
    ...


class FieldCreate(FieldBase):
    ...


class FieldView(IdMixin, TagsViewMixin, FieldBase):
    class Config:
        orm_mode = True


class FieldReference(ReferenceMixinFactory(FieldView)):
    ...
