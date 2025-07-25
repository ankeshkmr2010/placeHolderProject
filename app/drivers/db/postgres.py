# app/db/postgres.py
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.drivers.configs.config import Config
from app.drivers.db.base import BaseDBClient

class PostgresClient(BaseDBClient):
    def __init__(self):
        self.engine = create_async_engine(Config.POSTGRES_URL, echo=False)
        self.sessionmaker = async_sessionmaker(bind=self.engine, expire_on_commit=False)

    async def connect(self) -> AsyncSession:
        return self.sessionmaker()

    async def close(self):
        await self.engine.dispose()
