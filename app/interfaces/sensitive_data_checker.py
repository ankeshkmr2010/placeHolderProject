from abc import ABC, abstractmethod

from pydantic import BaseModel, Field
from typing import List


class FlaggedSensitiveData(BaseModel):
    text_snippet:str = Field("Snippet of text containing sensitive data")
    data_type: str = Field("Type of sensitive data (e.g., SSN, credit card, email)")
    start_index: int = Field("Start index of the sensitive data in the text")
    end_index: int = Field("End index of the sensitive data in the text")



class SensitiveDataChecker(ABC):
    """
    Abstract base class for checking sensitive data in a given text.
    """

    @abstractmethod
    async def check(self, text: str) -> List[FlaggedSensitiveData]:
        """
        Check if the given text contains sensitive data.

        :param text: The text to check for sensitive data.
        :return: True if the text contains sensitive data, False otherwise.
        """
        pass

    @abstractmethod
    async def _check_for_ssn(self,text :str) ->List[FlaggedSensitiveData]:
        pass

    @abstractmethod
    async def _check_for_credit_card(self, text:str) -> List[FlaggedSensitiveData]:
        pass


    @abstractmethod
    async def _check_for_email(self, text:str)->List[FlaggedSensitiveData]:
        pass