from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker


class SQLalchemyStorage:
    engine: AsyncEngine
    sessionmaker: async_sessionmaker

    def __init__(self, engine: AsyncEngine) -> None:
        self.engine = engine
        self.sessionmaker = async_sessionmaker(engine, expire_on_commit=False)

    @classmethod
    def from_url(cls, url: str) -> "SQLalchemyStorage":
        from sqlalchemy.ext.asyncio import create_async_engine
        engine = create_async_engine(url)
        return cls(engine)

    def create_session(self) -> AsyncSession:
        return self.sessionmaker()

    async def __create_all(self) -> None:
        from data.models import BaseModel
        async with self.engine.begin() as conn:
            await conn.run_sync(BaseModel.metadata.create_all)

    def create_all(self) -> None:
        from asyncio import new_event_loop
        loop = new_event_loop()
        loop.run_until_complete(self.__create_all())
        loop.close()


__all__ = ["SQLalchemyStorage"]
