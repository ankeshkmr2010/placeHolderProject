from abc import ABC, abstractmethod
from typing import  List
from app.schemas.GetCompletionReq import GetCompletionReq


class LlmClientWrapper(ABC):
    @abstractmethod
    async def get_completion(self, req:GetCompletionReq) -> str:
        pass

    @abstractmethod
    async def execute_multiple_prompts_parallel(self, reqs:List[GetCompletionReq])-> List[str]:
        pass
