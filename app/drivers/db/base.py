# app/db/base.py
from abc import ABC, abstractmethod

class BaseDBClient(ABC):
    @abstractmethod
    async def connect(self):
        ...

    @abstractmethod
    async def close(self):
        ...


