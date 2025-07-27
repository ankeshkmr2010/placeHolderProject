from abc import ABC, abstractmethod
from typing import List


class PromptProcessor(ABC):
    """
    Abstract base class for processing prompts.

    This class defines the interface for generating prompts related to job description extraction
    and resume processing. Subclasses must implement the abstract methods to provide specific functionality.
    """

    @abstractmethod
    async def get_jd_extraction_prompt(self, jd_text: str) -> str:
        """
        Abstract method to generate a prompt for extracting job description criteria.

        Args:
            jd_text (str): The text of the job description.

        Returns:
            str: The generated prompt for job description extraction.
        """
        pass

    @abstractmethod
    async def get_resume_processing_prompt(self, criterion: List[str], resumes: List[str]) -> List[str]:
        """
        Abstract method to generate prompts for processing resumes based on given criteria.

        Args:
            criterion (List[str]): A list of criteria extracted from the job description.
            resumes (List[str]): A list of resume texts.

        Returns:
            List[str]: A list of generated prompts for processing the resumes.
        """
        pass