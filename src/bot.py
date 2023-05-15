import asyncio
import logging
import platform
from contextlib import suppress

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram_dialog import setup_dialogs

from config import settings
from middlewares.repository_middleware import setup_repos_middleware, create_superuser
from routers.main import main_router, register_stop_handler

if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

logging.basicConfig(level=logging.INFO)

if settings.STORAGE == "memory":
    from aiogram.fsm.storage.memory import MemoryStorage

    storage = MemoryStorage()


async def create_bot():
    _bot = Bot(token=settings.TG_TOKEN, parse_mode="HTML")
    common_commands = [
        BotCommand(command="/start", description="Начать диалог"),
        BotCommand(command="/help", description="Помощь"),
    ]

    await _bot.delete_webhook(drop_pending_updates=True)
    await _bot.set_my_commands(common_commands)
    return _bot


async def create_dispatcher() -> Dispatcher:
    dp = Dispatcher(storage=storage)
    _repos_middleware = await setup_repos_middleware(dp)
    await create_superuser(_repos_middleware.users_repository,
                           _repos_middleware.roles_repository,
                           settings.SUPERUSER_ID)

    dp.include_router(main_router)
    register_stop_handler(dp)

    setup_dialogs(dp)

    return dp


async def main():
    bot = await create_bot()
    dispatcher = await create_dispatcher()
    await dispatcher.start_polling(bot, skip_updates=True)


if __name__ == '__main__':
    with suppress(KeyboardInterrupt):
        asyncio.run(main())
