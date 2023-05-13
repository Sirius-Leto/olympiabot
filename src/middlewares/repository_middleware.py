from typing import Callable, Awaitable, Union
from typing import TypeVar

from aiogram import BaseMiddleware, Dispatcher, Router
from aiogram.types import Message

from data.repositories.roles import RolesRepository
from data.repositories.users import UserRepository

Repository = TypeVar("Repository")


class RepositoryMiddleware(BaseMiddleware):
    repository_keys: list[str]
    users_repository: UserRepository
    roles_repository: RolesRepository

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


def setup_repos_middleware(target: Union[Router, Dispatcher]) -> None:
    from data.storages.sqldatabase import SQLalchemyStorage
    from data.schemas.users import UserCreate
    from config import settings

    storage = SQLalchemyStorage.from_url(settings.SQLITE_URL)
    storage.create_all()

    users_repository = UserRepository(storage)
    roles_repository = RolesRepository(storage)

    from asyncio import run
    user = run(users_repository.create_if_not_exists(UserCreate(tg_id=settings.SUPERUSER_ID)))
    if not user:
        user = run(users_repository.get_by_tg_id(settings.SUPERUSER_ID))
    run(roles_repository.setup_role(user.id, "superuser"))
    print(f"Superuser: {user}")

    middleware = RepositoryMiddleware(users_repository=users_repository,
                                      roles_repository=roles_repository)

    target.message.middleware(middleware)


__all__ = ["RepositoryMiddleware", "setup_repos_middleware"]
