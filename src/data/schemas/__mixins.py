from .__base import BaseModel
from datetime import datetime
from typing import Optional, List


class IdMixin(BaseModel):
    id: Optional[int] = None


class NameDescriptionMixin(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class TimestampMixin(BaseModel):
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


from .tags import TagReference, TagView


class TagsMixin:
    tags: Optional[List[TagReference]] = None


class TagsViewMixin:
    tags: Optional[List[TagView]] = None


__all__ = [
    "IdMixin",
    "NameDescriptionMixin",
    "TimestampMixin",
    "TagsMixin",
    "TagsViewMixin",
    "TagReference",
]
