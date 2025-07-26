from app.interfaces.prompt_exec import PromptProcessor
from jinja2 import Template

from app.repos.prompt_exec.prompts import Prompts


class PromptProcessorImpl(PromptProcessor):
    """
    Implementation of the PromptProcessor interface for handling prompt generation.
    This class provides methods to generate prompts for job description extraction and resume processing.
    """

    async def get_jd_extraction_prompt(self, jd_text: str) -> str:
        return Template(Prompts.JD_EXTRACTION_PROMPT).render(jd_text=jd_text)

    async def get_resume_processing_prompt(self, criterion: list[str], resumes: list[str]) -> list[str]:
        prompts = []
        for resume in resumes:
            prompt = Template(Prompts.RESUME_PROCESSING_PROMPT).render(
                criteria=", ".join(criterion), resume=resume
            )
            prompts.append(prompt)
        return prompts

