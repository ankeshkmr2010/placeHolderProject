from abc import ABC
from typing import List

from fastapi import UploadFile

from app.interfaces.file_parser import Fileparser
from app.interfaces.hiring_processor import HiringProcessor
from app.interfaces.llm_wrapper import LlmClientWrapper
from app.interfaces.prompt_exec import PromptProcessor
from app.schemas.get_completion_reqs import GetCompletionReq
from app.schemas.jd_criteria import JDCriteria


class HiringProcessorImpl(HiringProcessor):
    def __init__(self, file_parser:Fileparser,prompt_processor:PromptProcessor, llm_client:LlmClientWrapper):
        self.promptExecutor: PromptProcessor = prompt_processor
        self.file_parser: Fileparser = file_parser
        self.llm_client:LlmClientWrapper = llm_client

    async def extract_jd_criteria(self, file: UploadFile) -> JDCriteria:
        # parse file
        jd_text =await self.file_parser.parse_file(file)
        # get prompt for jd extraction
        if not jd_text:
            return JDCriteria()
        prompt = await self.promptExecutor.get_jd_extraction_prompt(jd_text)
        # call llm client
        response = await self.llm_client.get_completion(
            GetCompletionReq(
                model="gpt-4o-2024-08-06",
                prompt=prompt,
                max_tokens=1000
            ),
            text_format=JDCriteria
        )
        return response

    async def rank_resumes(self, jd_criteria: List[str], resumes: List[UploadFile]) -> List[dict]:
        pass