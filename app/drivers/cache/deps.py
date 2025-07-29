from contextlib import asynccontextmanager

from app.drivers.cache.redis import RedisCache
from app.drivers.configs.config import Config


@asynccontextmanager
async def get_redis_client():
    client = RedisCache(Config.REDIS_URI)
    await client.connect()
    try:
        yield client
    finally:
        await client.close()