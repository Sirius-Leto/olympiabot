from sqlalchemy import (select, update, delete)
from sqlalchemy.dialects.sqlite import insert

from data.models import EventModel, EventTypeModel, FieldModel, LevelModel, SubjectModel, TagModel
# from data.schemas.
from data.storages.sqldatabase import AbstractSQLAlchemyStorage

from abc import ABC, abstractmethod


class AbstractOlympiadsRepository(ABC):

    # ====== Event ======
    @abstractmethod
    def create_event(self, event: EventModel) -> EventModel:
        ...

    # ====== EventType ======
    @abstractmethod
    def create_event_type(self, event_type: EventTypeModel) -> EventTypeModel:
        ...




class OlympiadsRepository(AbstractOlympiadsRepository):
    storage: AbstractSQLAlchemyStorage

    def __init__(self, storage: AbstractSQLAlchemyStorage) -> None:
        self.storage = storage


__all__ = ["OlympiadsRepository", "AbstractOlympiadsRepository"]
