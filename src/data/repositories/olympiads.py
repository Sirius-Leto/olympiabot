from abc import ABC, abstractmethod

from sqlalchemy.orm import selectinload, joinedload, subqueryload, lazyload, noload

from data.schemas import EventView, SubjectView, GradeView, LevelView
from data.models import EventModel, SubjectModel, GradeModel, LevelModel, EventTypeModel
from data.storages.sqldatabase import AbstractSQLAlchemyStorage

from sqlalchemy import select


class AbstractOlympiadsRepository(ABC):

    # ====== Event ======
    @abstractmethod
    async def get_event(self, event_id: int) -> EventView:
        ...

    @abstractmethod
    async def filter_olympiads(self, grades: list[str], subjects: list[str], levels: list[str]) -> list[
        tuple[str, int]]:
        ...

    # ====== Subject ======

    @abstractmethod
    async def get_subject(self, subject_id: int) -> SubjectView:
        ...

    @abstractmethod
    async def get_subjects_by_names(self, subject_names: list[str]) -> list[SubjectView]:
        ...

    @abstractmethod
    async def get_all_subjects(self) -> list[SubjectView]:
        ...

    # ====== Grade ======
    @abstractmethod
    async def get_grade(self, grade_id: int) -> GradeView:
        ...

    @abstractmethod
    async def get_grades_by_names(self, grade_names: list[str]) -> list[GradeView]:
        ...

    @abstractmethod
    async def get_all_grades(self) -> list[GradeView]:
        ...

    # ====== Level ======
    @abstractmethod
    async def get_level(self, level_id: int) -> LevelView:
        ...

    @abstractmethod
    async def get_levels_by_names(self, level_names: list[str]) -> list[LevelView]:
        ...


class OlympiadsRepository(AbstractOlympiadsRepository):
    storage: AbstractSQLAlchemyStorage

    def __init__(self, storage: AbstractSQLAlchemyStorage) -> None:
        self.storage = storage

    # ====== Event ======
    async def get_event(self, event_id: int) -> EventView:
        async with self.storage.create_session() as session:
            stmt = select(EventModel).options(
                selectinload(EventModel.tags),
                selectinload(EventModel.subjects).selectinload(SubjectModel.tags),
                selectinload(EventModel.grades),
                selectinload(EventModel.levels).selectinload(LevelModel.tags),
                joinedload(EventModel.event_type).selectinload(EventTypeModel.tags),
            )
            r = await session.scalar(stmt.where(EventModel.id == event_id))
            return EventView.from_orm(r)

    async def filter_olympiads(self,
                               grades: list[str] = None,
                               subjects: list[str] = None,
                               levels: list[str] = None) -> list[tuple[str, int]]:
        async with self.storage.create_session() as session:
            stmt = select(EventModel).options(
                selectinload(EventModel.tags),
                selectinload(EventModel.subjects),
                selectinload(EventModel.grades),
                selectinload(EventModel.levels),
            )

            if grades:
                stmt = stmt.filter(EventModel.grades.any(GradeModel.name.in_(grades)))
            if subjects:
                stmt = stmt.filter(EventModel.subjects.any(SubjectModel.name.in_(subjects)))
            if levels:
                stmt = stmt.filter(EventModel.levels.any(LevelModel.name.in_(levels)))

            r = await session.scalars(stmt)
            events = r.all()
            return [(event.name, event.id) for event in events]

    # ====== Subject ======
    async def get_subject(self, subject_id: int) -> SubjectView:
        async with self.storage.create_session() as session:
            r = await session.get(SubjectModel, subject_id)
            return SubjectView.from_orm(r)

    async def get_subjects_by_names(self, subject_names: list[str]) -> list[SubjectView]:
        async with self.storage.create_session() as session:
            r = await session.scalars(select(SubjectModel)
                                      .filter(SubjectModel.name.in_(subject_names))
                                      .options(selectinload(SubjectModel.tags)))
            return [SubjectView.from_orm(subject) for subject in r.all()]

    async def get_all_subjects(self) -> list[SubjectView]:
        async with self.storage.create_session() as session:
            r = await session.scalars(select(SubjectModel)
                                      .options(selectinload(SubjectModel.tags)))
            return [SubjectView.from_orm(subject) for subject in r.all()]

    # ====== Grade ======
    async def get_grade(self, grade_id: int) -> GradeView:
        async with self.storage.create_session() as session:
            r = await session.get(GradeModel, grade_id)
            return GradeView.from_orm(r)

    async def get_grades_by_names(self, grade_names: list[str]) -> list[GradeView]:
        async with self.storage.create_session() as session:
            r = await session.scalars(select(GradeModel)
                                      .filter(GradeModel.name.in_(grade_names)))
            return [GradeView.from_orm(grade) for grade in r.all()]

    async def get_all_grades(self) -> list[GradeView]:
        async with self.storage.create_session() as session:
            r = await session.scalars(select(GradeModel))
            return [GradeView.from_orm(grade) for grade in r.all()]

    # ====== Level ======
    async def get_level(self, level_id: int) -> LevelView:
        async with self.storage.create_session() as session:
            r = await session.get(LevelModel, level_id)
            return LevelView.from_orm(r)

    async def get_levels_by_names(self, level_names: list[str]) -> list[LevelView]:
        async with self.storage.create_session() as session:
            r = await session.scalars(select(LevelModel)
                                      .filter(LevelModel.name.in_(level_names))
                                      .options(selectinload(LevelModel.tags)))
            return [LevelView.from_orm(level) for level in r.all()]


__all__ = ["OlympiadsRepository", "AbstractOlympiadsRepository"]
