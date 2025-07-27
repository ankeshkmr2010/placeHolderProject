from contextlib import AsyncExitStack

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy import text

from app.drivers.cache.deps import get_redis_client
from app.drivers.db.deps import get_postgres_client, get_mongo_client

router = APIRouter()

@router.get("/")
async def say_hi():
    return "Hi"

@router.get("/bothDb")
async def get_both():
    async with AsyncExitStack() as stack:
        pg = await stack.enter_async_context(get_postgres_client())
        mongo = await stack.enter_async_context(get_mongo_client())

        result = await pg.execute(text('SELECT 1'))
        mongo_collections = await mongo.list_collection_names()

        return {
            "postgres_result": result.scalar(),
            "mongo_collections": mongo_collections
        }

@router.get("/postgres")
async def get_postgres_data(pg=Depends(get_postgres_client)):
    async with AsyncExitStack() as stack:
        pg = await stack.enter_async_context(pg)
        result = await pg.execute(text('SELECT 1'))
        return {"postgres_result": result.scalar()}

@router.get("/mongo")
async def get_mongo_data(mongo=Depends(get_mongo_client)):
    async with AsyncExitStack() as stack:
        mongo = await stack.enter_async_context(mongo)
        collections = await mongo.list_collection_names()
        return {"mongo_collections": collections}

@router.put("/redis")
async def set_redis_data(key: str, value: str, redis=Depends(get_redis_client)):
    async with AsyncExitStack() as stack:
        redis = await stack.enter_async_context(redis)
        await redis.set(key, value)
        return {"status": "success", "key": key, "value": value}

@router.get("/redis")
async def get_redis_data(key: str, redis=Depends(get_redis_client)):
    async with AsyncExitStack() as stack:
        redis = await stack.enter_async_context(redis)
        value = await redis.get(key)
        return {"key": key, "value": value.decode() if value else None}

@router.get("/redis/ping")
async def ping_redis(redis=Depends(get_redis_client)):
    async with AsyncExitStack() as stack:
        redis = await stack.enter_async_context(redis)
        await redis.ping()
        return {"status": "Redis is connected!"}
