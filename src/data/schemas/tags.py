from .__base import BaseModel
from .__mixins import IdMixin, NameDescriptionMixin, TimestampMixin


class TagBase(TimestampMixin, NameDescriptionMixin, BaseModel):
    ...


class TagCreate(TagBase):
    ...


class TagView(IdMixin, TagBase):
    class Config:
        orm_mode = True


class TagReference(BaseModel):
    id: int
