import asyncio
from typing import List

from fastapi import UploadFile

from app.interfaces.file_parser import Fileparser
from app.interfaces.evaluator_engine import EvaluatorEngine
from app.interfaces.llm_wrapper import LlmClientWrapper
from app.interfaces.prompt_exec import PromptProcessor
from app.schemas.get_completion_reqs import GetCompletionReq
from app.schemas.jd_criteria import JDCriteria
import tempfile
import csv

from app.schemas.resume_eval_result import ResumeEvalResponse


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

    async def rank_resumes(self, jd_criteria: JDCriteria, resumes: List[UploadFile]) -> tempfile.NamedTemporaryFile:
        # parse resumes
        text_tasks = [self.file_parser.parse_file(resume) for resume in resumes]
        texts = await asyncio.gather(*text_tasks)
        prompt = await self.promptExecutor.get_resume_processing_prompt(jd_criteria.criteria, texts)
        # call llm client
        reqs = [GetCompletionReq(model="gpt-4o-2024-08-06", prompt=p) for p in prompt]
        responses = await self.llm_client.execute_multiple_prompts_parallel(reqs, text_format=ResumeEvalResponse)
        # write responses to a file

        temp_file = tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.csv', newline='')
        csv_writer = csv.writer(temp_file)

        # Write headers and responses to the CSV file
        header_row = ["CandidateName"] + jd_criteria.criteria + ["TotalScore"]
        print(f"Header Row: {header_row}")
        csv_writer.writerow(header_row)

        for response in responses:
            if isinstance(response, Exception):
                print(f"Error processing response: {response}")
                continue
            if isinstance(response, ResumeEvalResponse):
                data_row = [response.name] + [score.score for score in response.criteria_wise_score] + [response.score]
                csv_writer.writerow(data_row)

        temp_file.close()

        return temp_file

