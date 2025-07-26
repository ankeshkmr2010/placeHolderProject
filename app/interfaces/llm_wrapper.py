import typing
from abc import ABC, abstractmethod
from typing import  List
from app.schemas.get_completion_reqs import GetCompletionReq


class LlmClientWrapper(ABC):
    @abstractmethod
    async def get_completion(self, req:GetCompletionReq, text_format:type = typing.Text) -> any:
        pass

    @abstractmethod
    async def execute_multiple_prompts_parallel(self, reqs:List[GetCompletionReq], text_format:type = typing.Text)-> List[any]:
        pass
