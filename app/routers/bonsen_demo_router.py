from contextlib import AsyncExitStack
from typing import List

from fastapi import APIRouter, UploadFile, File, Form
from fastapi.params import Depends

from app.drivers.cache.deps import get_redis_client
from app.repos.deps import get_file_parser, get_evaluator_engine
from app.routers.base_router import get_redis_data
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
async def extract_criteria(ufile: UploadFile, redis=Depends(get_redis_client)):
    async with AsyncExitStack() as stack:
        redis = await stack.enter_async_context(redis)
        if not redis:
            raise ValueError("Redis client is not available")
        evaluatort_engine =  get_evaluator_engine(redis)
        criteria = await evaluatort_engine.extract_jd_criteria(ufile)
        return criteria

@bonsen_router.post("/score-resumes")
async def score_resumes(
    criteria: List[str]= Form(...),
    resumes: list[UploadFile] = File(...),
    redis=Depends(get_redis_client)
):
    async with AsyncExitStack() as stack:
        redis = await stack.enter_async_context(redis)
        if not redis:
            raise ValueError("Redis client is not available")
        if redis is None:
            raise ValueError("Redis client is not available")
        evaluator_engine = get_evaluator_engine(redis)
        for cri in criteria:
            if not cri:
                raise ValueError("Criteria cannot be empty")
        jd_criteria = JDCriteria(criteria=criteria)
        score_file = await evaluator_engine.rank_resumes(jd_criteria, resumes)
        return {"score_file": score_file.name}

