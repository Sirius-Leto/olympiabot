import asyncio
from aiogram import Bot, Dispatcher
from config import settings

from routers.main import router

# try to setup the storage
try:
    from aiogram.fsm.storage.redis import RedisStorage, Redis

    rd = Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB,
        password=settings.REDIS_PASSWORD,
    )

    storage = RedisStorage(redis=rd)

except Exception as e:
    from aiogram.fsm.storage.memory import MemoryStorage

    storage = MemoryStorage()


async def main():
    bot = Bot(token=settings.TG_TOKEN, parse_mode="HTML")
    dp = Dispatcher(storage=storage)
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
