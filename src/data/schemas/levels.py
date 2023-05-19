from .__base import BaseModel
from .__mixins import IdMixin, TimestampMixin, NameDescriptionMixin, TagsMixin, TagsViewMixin, ReferenceMixinFactory


class LevelBase(TimestampMixin, NameDescriptionMixin, TagsMixin, BaseModel):
    ...


class LevelCreate(LevelBase):
    ...


class LevelView(IdMixin, TagsViewMixin, LevelBase):
    class Config:
        orm_mode = True


class LevelReference(ReferenceMixinFactory(LevelView)):
    ...
