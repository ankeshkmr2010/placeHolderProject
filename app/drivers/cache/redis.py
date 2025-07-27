from typing import Any

import redis.asyncio as redis

from app.drivers.cache.base import BaseCache

connection_string = "redis://:@localhost:6379/0"


class RedisCache(BaseCache):
    def __init__(self):
        self.client = redis.from_url(connection_string)
        print(f"Connecting to Redis at {connection_string}")

    async def connect(self):
        await self.client.ping()

    async def close(self):
        await self.client.close()

    async def get(self, key: str):
        return await self.client.get(key)

    async def set(self, key: str, value: Any, ex: int = None):
        return await self.client.set(key, value, ex=ex)

    async def delete(self, key: str):
        return await self.client.delete(key)

    async def ping(self):
        return await self.client.ping()