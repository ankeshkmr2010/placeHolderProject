import typing
from abc import ABC, abstractmethod
from typing import List

from pydantic import BaseModel

from app.schemas.get_completion_reqs import GetCompletionReq


class LlmClientWrapper(ABC):
    """
    Abstract base class for an LLM (Large Language Model) Client Wrapper.

    This class defines the interface for interacting with an LLM client.
    Subclasses must implement the abstract methods to provide specific functionality.
    """

    @abstractmethod
    async def execute_prompt(self, req: GetCompletionReq, text_format: BaseModel) -> any:
        """
        Abstract method to get a completion response from the LLM client.

        Args:
            req (GetCompletionReq): The request object containing the prompt and other parameters.
            text_format (BaseModel): The format in which the response should be structured.

        Returns:
            any: The completion response from the LLM client.
        """
        pass

    @abstractmethod
    async def execute_multiple_prompts_parallel(
        self, reqs: List[GetCompletionReq], text_format: type = typing.Text
    ) -> List[any]:
        """
        Abstract method to execute multiple prompts in parallel and get their responses.

        Args:
            reqs (List[GetCompletionReq]): A list of request objects containing prompts and parameters.
            text_format (type, optional): The format in which the responses should be structured. Defaults to typing.Text.

        Returns:
            List[any]: A list of completion responses from the LLM client.
        """
        pass