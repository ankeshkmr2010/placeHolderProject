from abc import ABC, abstractmethod
from typing import List


class PromptProcessor(ABC):
    @abstractmethod
    async def get_jd_extraction_prompt(self, jd_text:str) -> str:
        pass

    @abstractmethod
    async def get_resume_processing_prompt(self, criterion:List[str], resumes:List[str]) -> list[str]:
        pass
