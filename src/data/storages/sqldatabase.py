from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker
from abc import ABC, abstractmethod


class AbstractSQLAlchemyStorage(ABC):
    @abstractmethod
    def create_session(self) -> AsyncSession:
        ...

    @abstractmethod
    async def create_all(self) -> None:
        ...


class SQLiteStorage(AbstractSQLAlchemyStorage):
    engine: AsyncEngine
    sessionmaker: async_sessionmaker

    def __init__(self, engine: AsyncEngine) -> None:
        self.engine = engine
        self.sessionmaker = async_sessionmaker(engine, expire_on_commit=False)

    @classmethod
    def from_url(cls, url: str) -> "SQLiteStorage":
        from sqlalchemy.ext.asyncio import create_async_engine
        engine = create_async_engine(url)
        return cls(engine)

    def create_session(self) -> AsyncSession:
        return self.sessionmaker()

    async def create_all(self) -> None:
        from data.models import BaseModel
        async with self.engine.begin() as conn:
            await conn.run_sync(BaseModel.metadata.create_all)


__all__ = ["SQLiteStorage", "AbstractSQLAlchemyStorage"]
