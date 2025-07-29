# app/db/deps.py
from contextlib import asynccontextmanager

from app.drivers.db.mongo import MongoClient
from app.drivers.db.postgres import PostgresClient


@asynccontextmanager
async def get_postgres_client():
    client = PostgresClient()
    db_session = await client.connect()
    try:
        yield db_session
    finally:
        await db_session.close()


@asynccontextmanager
async def get_mongo_client():
    client = MongoClient()
    db = await client.connect()
    try:
        yield db
    finally:
        await client.close()


@asynccontextmanager
async def get_db_clients():
    pg_client = PostgresClient()
    mongo_client = MongoClient()
    pg_session = await pg_client.connect()
    mongo_db = await mongo_client.connect()
    try:
        yield {
            "postgres": pg_session,
            "mongo": mongo_db
        }
    finally:
        await pg_session.close()
        await mongo_client.close()
