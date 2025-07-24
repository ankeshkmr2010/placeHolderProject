from contextlib import AsyncExitStack

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy import text

from app.drivers.db.deps import get_db_clients, get_postgres_client, get_mongo_client

router = APIRouter()

@router.get("/")
async def list_items():
    return [{"id": 1, "name": "Foo"}, {"id": 2, "name": "Bar"}]

@router.get("/both")
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
