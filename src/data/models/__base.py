from typing import Any, Dict

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.types import JSON


class Base(DeclarativeBase):
    type_annotation_map = {
        Dict[str, Any]: JSON,
        dict[str, ...]: JSON
    }
