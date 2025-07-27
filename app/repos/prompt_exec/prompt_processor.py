from app.interfaces.prompt_exec import PromptProcessor
from jinja2 import Template

from app.repos.prompt_exec.prompts import Prompts


class PromptProcessorImpl(PromptProcessor):
    """
    Implementation of the PromptProcessor interface that generates prompts for job description extraction and resume processing.
    This class uses Jinja2 templates to render prompts based on the provided job description text and resumes.
    """

    async def get_jd_extraction_prompt(self, jd_text: str) -> str:
        """
        Generates a prompt for extracting job description criteria from the provided job description text.
        :param jd_text:
        :return str: A prompt string formatted with the job description text.
        """
        return Template(Prompts.JD_EXTRACTION_PROMPT).render(jd_text=jd_text)

    async def get_resume_processing_prompt(self, criterion: list[str], resumes: list[str]) -> list[str]:
        """
        :param criterion:
        :param resumes:
        :return list[str]: A list of prompts for processing each resume based on the provided criteria.
        """
        prompts = []
        for resume in resumes:
            prompt = Template(Prompts.RESUME_PROCESSING_PROMPT).render(
                criteria=criterion, resume=resume
            )
            prompts.append(prompt)
        return prompts

