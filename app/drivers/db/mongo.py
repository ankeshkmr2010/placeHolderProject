# app/db/mongo.py
from motor.motor_asyncio import AsyncIOMotorClient

from app.drivers.configs.config import Config
from app.drivers.db.base import BaseDBClient


class MongoClient(BaseDBClient):
    def __init__(self):
        self.client = AsyncIOMotorClient(Config.MONGO_URI)
        self.db = self.client[Config.MONGO_DBNAME]

    async def connect(self):
        return self.db

    async def close(self):
        self.client.close()
