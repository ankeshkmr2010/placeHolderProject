from abc import ABC, abstractmethod
from typing import List
from fastapi import UploadFile

from app.schemas.jd_criteria import JDCriteria


class HiringProcessor(ABC):
    @abstractmethod
    async def extract_jd_criteria(self, file: UploadFile) ->JDCriteria:
        pass


    @abstractmethod
    async def rank_resumes(self, jd_criteria: JDCriteria, resumes: List[UploadFile]) -> List[dict]:
        pass
