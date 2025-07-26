from typing import List

from fastapi import APIRouter, UploadFile



from app.repos.deps import get_file_parser, get_evaluator_engine
from app.schemas.jd_criteria import JDCriteria

bonsen_router = APIRouter()

@bonsen_router.get("/ping")
async def ping():
    return {"message": "pong"}

@bonsen_router.post("/parse-file")
async def parse_input(ufile: UploadFile):
    file_parser = get_file_parser()
    a = await file_parser.parse_file(ufile)
    return {"file_content": a}


@bonsen_router.post("/extract-criteria")
async def extract_criteria(ufile: UploadFile):
    evaluatort_engine =  get_evaluator_engine()
    criteria = await evaluatort_engine.extract_jd_criteria(ufile)
    return criteria

@bonsen_router.post("/score-resumes")
async def score_resumes(
    criteria: List[str],
    resumes: list[UploadFile],
):
    evaluator_engine = get_evaluator_engine()
    jd_criteria = JDCriteria(criteria=criteria)
    scores = await evaluator_engine.rank_resumes(jd_criteria, resumes)
    return scores
