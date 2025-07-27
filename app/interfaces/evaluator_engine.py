import tempfile
from abc import ABC, abstractmethod
from typing import List

from fastapi import UploadFile

from app.schemas.jd_criteria import JDCriteria


class EvaluatorEngine(ABC):
    """
    Abstract base class for an Evaluator Engine.

    This class defines the interface for evaluating job descriptions and ranking resumes.
    Subclasses must implement the abstract methods to provide specific functionality.
    """

    @abstractmethod
    async def extract_jd_criteria(self, file: UploadFile) -> JDCriteria:
        """
        Extracts job description criteria from the provided file.

        Args:
            file (UploadFile): The uploaded file containing the job description.

        Returns:
            JDCriteria: The extracted job description criteria.
        """
        pass

    @abstractmethod
    async def rank_resumes(self, jd_criteria: JDCriteria, resumes: List[UploadFile]) -> tempfile.NamedTemporaryFile:
        """
        Ranks resumes based on the provided job description criteria.

        Args:
            jd_criteria (JDCriteria): The job description criteria used for ranking.
            resumes (List[UploadFile]): A list of uploaded resume files.

        Returns:
            tempfile.NamedTemporaryFile: A temporary file containing the ranked resumes.
        """
        pass