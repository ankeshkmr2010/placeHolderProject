from contextlib import asynccontextmanager

from app.drivers.cache.redis import RedisCache


@asynccontextmanager
async def get_redis_client():
    client = RedisCache()
    await client.connect()
    try:
        yield client
    finally:
        await client.close()