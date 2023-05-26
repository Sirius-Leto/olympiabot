from typing import Callable, Awaitable, Union
from typing import TypeVar

from aiogram import BaseMiddleware, Dispatcher, Router
from aiogram.types import Message

from data.repositories.roles import AbstractRolesRepository
from data.repositories.users import AbstractUserRepository
from data.repositories.olympiads import AbstractOlympiadsRepository

Repository = TypeVar("Repository")


class RepositoryMiddleware(BaseMiddleware):
    repository_keys: list[str]
    users_repository: AbstractUserRepository
    roles_repository: AbstractRolesRepository
    olympiads_repository: AbstractOlympiadsRepository

    def __init__(self, **repositories: Repository) -> None:
        super().__init__()
        self.repository_keys = []

        for key, value in repositories.items():
            self.repository_keys.append(key)
            setattr(self, key, value)

    async def __call__(
            self,
            handler: Callable[[Message, dict[str, ...]], Awaitable[...]],
            event: Message,
            data: dict[str, ...]
    ) -> ...:
        data.update({key: getattr(self, key) for key in self.repository_keys})
        result = await handler(event, data)
        return result

    def copy(self) -> "RepositoryMiddleware":
        return RepositoryMiddleware(**{key: getattr(self, key) for key in self.repository_keys})


async def create_superuser(users_repository: AbstractUserRepository,
                           roles_repository: AbstractRolesRepository,
                           tg_id: int) -> None:
    from data.schemas.users import UserCreate

    await (users_repository.create_if_not_exists(UserCreate(tg_id=tg_id)))
    user = await users_repository.get_by_tg_id(tg_id)
    print(f"User: {user}")
    await roles_repository.set_role(tg_id, "superuser")
    print(f"Superuser: @{tg_id}")


async def setup_repos_middleware(target: Union[Router, Dispatcher]) -> RepositoryMiddleware:
    from data.storages.sqldatabase import SQLiteStorage
    from data.repositories.roles import RoleRepository
    from data.repositories.users import UserRepository
    from config import settings

    storage = SQLiteStorage.from_url(settings.SQLITE_URL)
    print(f"Storage: {storage.get_path()}")
    await storage.create_all()

    from data.repositories.olympiads import OlympiadsRepository
    olympiads_repository = OlympiadsRepository(storage)
    users_repository = UserRepository(storage)
    roles_repository = RoleRepository(storage)
    await roles_repository.init_cache()

    middleware = RepositoryMiddleware(users_repository=users_repository,
                                      roles_repository=roles_repository,
                                      olympiads_repository=olympiads_repository)

    target.message.middleware(middleware)
    target.callback_query.middleware(middleware)

    return middleware


__all__ = ["RepositoryMiddleware", "setup_repos_middleware", "create_superuser"]
