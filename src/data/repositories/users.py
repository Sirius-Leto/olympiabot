from sqlalchemy import (select, update, delete)
from sqlalchemy.dialects.sqlite import insert

from data.models import UserModel
from data.schemas.users import UserView, UserCreate
from data.storages.sqldatabase import AbstractSQLAlchemyStorage

from abc import ABC, abstractmethod


class AbstractUserRepository(ABC):
    @abstractmethod
    async def create(self, user_id: int) -> UserView:
        ...

    @abstractmethod
    async def get_by_tg_id(self, tg_id: int) -> UserView:
        ...

    @abstractmethod
    async def get_all(self) -> list[UserView]:
        ...

    @abstractmethod
    async def add(self, user: UserCreate) -> None:
        ...

    @abstractmethod
    async def create_if_not_exists(self, user: UserCreate):
        ...

    @abstractmethod
    async def update(self, user: UserCreate) -> None:
        ...

    @abstractmethod
    async def delete(self, user_id: int) -> None:
        ...


class UserRepository(AbstractUserRepository):
    storage: AbstractSQLAlchemyStorage

    def __init__(self, storage: AbstractSQLAlchemyStorage) -> None:
        self.storage = storage

    async def create(self, user_id: int) -> UserView:
        async with self.storage.create_session() as session:
            r = await session.get(UserModel, user_id)
            return UserView.from_orm(r)

    async def get_by_tg_id(self, tg_id: int) -> UserView:
        async with self.storage.create_session() as session:
            r = await session.scalar(select(UserModel).where(UserModel.tg_id == tg_id))
            return UserView.from_orm(r)

    async def get_all(self) -> list[UserView]:
        async with self.storage.create_session() as session:
            r = await session.execute(select(UserModel))
            return [UserView.from_orm(i) for i in r.scalars()]

    async def add(self, user: UserCreate) -> None:
        async with self.storage.create_session() as session:
            session.add(UserModel(**user.dict()))
            await session.commit()

    async def create_if_not_exists(self, user: UserCreate):
        async with self.storage.create_session() as session:
            query = insert(UserModel).values(user.dict())
            query = query.on_conflict_do_nothing(index_elements=[UserModel.tg_id])

            await session.execute(query)
            await session.commit()

    async def update(self, user: UserCreate) -> None:
        async with self.storage.create_session() as session:
            await session.execute(update(UserModel).where(UserModel.tg_id == user.id).values(**user.dict()))
            await session.commit()

    async def delete(self, user_id: int) -> None:
        async with self.storage.create_session() as session:
            await session.execute(delete(UserModel).where(UserModel.tg_id == user_id))
            await session.commit()


__all__ = ["UserRepository", "AbstractUserRepository"]
