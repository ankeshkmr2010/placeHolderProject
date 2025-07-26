import asyncio
from typing import List

from fastapi import UploadFile
from pydantic import BaseModel, Field

from app.interfaces.file_parser import Fileparser
from app.interfaces.evaluator_engine import EvaluatorEngine
from app.interfaces.llm_wrapper import LlmClientWrapper
from app.interfaces.prompt_exec import PromptProcessor
from app.schemas.get_completion_reqs import GetCompletionReq
from app.schemas.jd_criteria import JDCriteria


class CriteriaScore(BaseModel):
    criteria_name: str = Field(description="Name of the criteria for which the resume is scored")
    score: float = Field(description="Score for the criteria, ranging from 0 to 5")

class ResumeEvalResponse(BaseModel):
    name: str = Field(description="Name of the candidate")
    score: float = Field(description="Sum of all criteria scores of the individual criteria")
    criteria_wise_score:List[CriteriaScore] = Field(description="List of scores for each criteria evaluated in the resume")




class EvaluatorEngineImpl(EvaluatorEngine):
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

    async def rank_resumes(self, jd_criteria: JDCriteria, resumes: List[UploadFile]) -> List[ResumeEvalResponse]:
        # parse resumes
        text_tasks = [self.file_parser.parse_file(resume) for resume in resumes]
        texts = await asyncio.gather(*text_tasks)
        prompt = await self.promptExecutor.get_resume_processing_prompt(jd_criteria.criteria, texts)
        # call llm client
        reqs = [GetCompletionReq(model="gpt-4o-2024-08-06", prompt=p) for p in prompt]
        responses = await self.llm_client.execute_multiple_prompts_parallel(reqs, text_format=ResumeEvalResponse)
        return responses

