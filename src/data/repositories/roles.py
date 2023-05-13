from asyncio import run
from collections import namedtuple
from enum import Enum
from typing import Union

from sqlalchemy import select
from sqlalchemy.dialects.sqlite import insert

from data.models import UserRolesModel, UserModel
from data.storages.sqldatabase import SQLalchemyStorage
from utilities import enum_ordering, UserDoesNotExistDB
import warnings


@enum_ordering
class UserRole(Enum):
    DEFAULT = 0
    MODERATOR = 1
    ADMIN = 2
    SUPERUSER = 3

    @classmethod
    def from_str(cls, role: str) -> "UserRole":
        return cls[role.upper()]


UserRoleDummies = namedtuple("UserRoleDummies", ["is_moderator", "is_admin", "is_superuser"])


class RolesRepository:
    storage: SQLalchemyStorage
    __cache: dict[int, UserRole]

    def __init__(self, storage: SQLalchemyStorage) -> None:
        self.storage = storage
        self.__cache = dict()

        run(self.__init_cache())

    async def __init_cache(self) -> None:
        async with self.storage.create_session() as session:
            query = select(UserRolesModel, UserModel).join(UserModel, UserRolesModel.user_id == UserModel.id)

            results = await session.execute(query)
            for user_role, user in results:
                tg_id = user.tg_id
                role = self.__get_role_enum_from_model(user_role)
                self.__cache_set_role(tg_id, role)

    @staticmethod
    def __get_role_enum_from_model(model: UserRolesModel) -> UserRole:
        role = UserRole.DEFAULT

        if model is None:
            return role

        if model.is_moderator:
            role = UserRole.MODERATOR
        elif model.is_admin:
            role = UserRole.ADMIN
        elif model.is_superuser:
            role = UserRole.SUPERUSER

        return role

    @staticmethod
    def __get_dummies_from_enum(role: Union[UserRole, str]) -> UserRoleDummies:

        if isinstance(role, str):
            role = UserRole.from_str(role)

        is_moderator = is_admin = is_superuser = False

        if role == UserRole.MODERATOR:
            is_moderator = True
        elif role == UserRole.ADMIN:
            is_admin = True
        elif role == UserRole.SUPERUSER:
            is_superuser = True

        return UserRoleDummies(is_moderator, is_admin, is_superuser)

    async def setup_role(self, db_id: int, role: Union[str, UserRole]) -> None:
        is_moderator, is_admin, is_superuser = self.__get_dummies_from_enum(role)

        async with self.storage.create_session() as session:
            user = await session.scalar(select(UserModel).where(UserModel.id == db_id))
            if user is None:
                warnings.warn(f"User with id {db_id} does not exist in database. Skipping setup roles.",
                              UserDoesNotExistDB)
                return

            tg_id = user.tg_id

            q = insert(UserRolesModel).values(user_id=db_id,
                                              is_moderator=is_moderator,
                                              is_admin=is_admin,
                                              is_superuser=is_superuser)

            q = q.on_conflict_do_update(index_elements=[UserRolesModel.user_id], set_={
                UserRolesModel.is_moderator: is_moderator,
                UserRolesModel.is_admin: is_admin,
                UserRolesModel.is_superuser: is_superuser,
            })

            await session.execute(q)
            await session.commit()

        self.__cache_set_role(tg_id, role)

    def __cache_get_role(self, tg_id: int) -> UserRole:
        return self.__cache.get(tg_id, None)

    def __cache_set_role(self, tg_id: int, role: Union[str, UserRole]) -> None:
        if isinstance(role, str):
            role = UserRole.from_str(role)
        self.__cache[tg_id] = role

    async def __get_role_from_db(self, tg_id: int) -> UserRole:
        async with self.storage.create_session() as session:
            query = (
                select(UserModel, UserRolesModel)
                .join(UserRolesModel, UserModel.id == UserRolesModel.user_id)
                .where(UserModel.tg_id == tg_id)
            )

            result = await session.scalar(query)

            if result is None:
                return UserRole.DEFAULT

            user, user_roles = result

            role = self.__get_role_enum_from_model(user_roles)
            self.__cache_set_role(tg_id, role)

        return role

    async def get_role(self, tg_id: int) -> UserRole:
        role = self.__cache_get_role(tg_id)

        if role is None:
            role = await self.__get_role_from_db(tg_id)
        return role


__all__ = ["RolesRepository", "UserRole"]
