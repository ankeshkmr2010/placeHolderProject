# app/db/mongo.py
from motor.motor_asyncio import AsyncIOMotorClient
from app.drivers.db.base import BaseDBClient

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "mydb"

class MongoClient(BaseDBClient):
    def __init__(self):
        self.client = AsyncIOMotorClient(MONGO_URI)
        self.db = self.client[DB_NAME]

    async def connect(self):
        return self.db

    async def close(self):
        self.client.close()
