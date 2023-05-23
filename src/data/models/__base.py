from typing import Any, Dict

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.types import JSON
from sqlalchemy.ext.asyncio import AsyncAttrs


class Base(AsyncAttrs, DeclarativeBase):
    type_annotation_map = {
        Dict[str, Any]: JSON,
        dict[str, ...]: JSON
    }


