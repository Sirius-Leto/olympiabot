from datetime import datetime
from typing import Optional, List

from .__base import BaseModel


class IdMixin(BaseModel):
    id: Optional[int] = None


class NameDescriptionMixin(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class TimestampMixin(BaseModel):
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


from .tags import TagReference, TagView


class TagsMixin(BaseModel):
    tags: Optional[List[TagReference]] = None


class TagsViewMixin(BaseModel):
    tags: Optional[List[TagView]] = None


def ReferenceMixinFactory(
        ViewModel: type,
) -> type:
    class ReferenceMixin(IdMixin, BaseModel):
        def __init__(self, id: int = None, instance: ViewModel = None):
            if instance:
                super().__init__(id=instance.id)
            else:
                super().__init__(id=id)

    return ReferenceMixin


__all__ = [
    "IdMixin",
    "NameDescriptionMixin",
    "TimestampMixin",
    "TagsMixin",
    "TagsViewMixin",
    "ReferenceMixinFactory",
]
