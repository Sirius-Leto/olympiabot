import logging
from contextlib import suppress

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand

from config import settings
from routers.main import main_router, register_stop_handler

logging.basicConfig(level=logging.INFO)

if settings.STORAGE == "memory":
    from aiogram.fsm.storage.memory import MemoryStorage

    storage = MemoryStorage()


async def main():
    bot = Bot(token=settings.TG_TOKEN)

    await (bot.set_my_commands([
        BotCommand(command="start", description="Запустить бота"),
        BotCommand(command="help", description="Помощь"),
    ]))

    dp = Dispatcher(storage=storage)
    dp.include_router(main_router)
    register_stop_handler(dp)
    # start long-polling
    await dp.start_polling(bot, skip_updates=True)


if __name__ == '__main__':
    from asyncio import run

    with suppress(KeyboardInterrupt):
        run(main())
