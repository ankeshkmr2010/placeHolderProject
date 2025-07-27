from typing import List

from pydantic import BaseModel, Field


class CriteriaScore(BaseModel):
    criteria_name: str = Field(description="Name of the criteria for which the resume is scored")
    score: float = Field(description="Score for the criteria, ranging from 0 to 5")
    evidence: str = Field(description="Evidence or justification for the score given to the criteria")


class ResumeEvalResponse(BaseModel):
    name: str = Field(description="Name of the candidate")
    score: float = Field(description="Sum of all criteria scores of the individual criteria")
    criteria_wise_score:List[CriteriaScore] = Field(description="List of scores for each criteria evaluated in the resume")
