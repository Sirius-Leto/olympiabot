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

    def __init__(self, id: int = None, instance: TagView = None):
        if instance:
            super().__init__(id=instance.id)
        else:
            super().__init__(id=id)

    class Config:
        orm_mode = True
