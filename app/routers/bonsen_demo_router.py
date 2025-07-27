from contextlib import AsyncExitStack
from typing import List

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.params import Depends
from starlette.responses import FileResponse

from app.constants import MAX_NUM_FILES
from app.drivers.cache.deps import get_redis_client
from app.repos.deps import get_file_parser, get_evaluator_engine
from app.schemas.jd_criteria import JDCriteria

# Create an API router for Bonsen-related endpoints
bonsen_router = APIRouter()


@bonsen_router.get("/ping")
async def ping():
    """
    Health check endpoint.

    Returns:
        dict: A dictionary containing a "pong" message.
    """
    return {"message": "pong"}


@bonsen_router.post("/parse-file")
async def parse_input(ufile: UploadFile):
    """
    Endpoint to parse the content of an uploaded file.

    Args:
        ufile (UploadFile): The uploaded file to be parsed.

    Returns:
        dict: A dictionary containing the parsed file content.
    """
    file_parser = get_file_parser()
    a = await file_parser.parse_file(ufile)
    return {"file_content": a}


@bonsen_router.post("/extract-criteria", response_model=JDCriteria)
async def extract_criteria(ufile: UploadFile, redis=Depends(get_redis_client)):
    """
    Endpoint to extract job description criteria from an uploaded file.

    Args:
        ufile (UploadFile): The uploaded file containing the job description.
        redis (Redis): Redis client dependency.

    Returns:
        JDCriteria: The extracted job description criteria.

    Raises:
        ValueError: If the Redis client is not available.
    """
    async with AsyncExitStack() as stack:
        redis = await stack.enter_async_context(redis)
        if not redis:
            raise HTTPException(status_code=500, detail="Redis client is not available")

        try:
            evaluatort_engine = get_evaluator_engine(redis)
            criteria = await evaluatort_engine.extract_jd_criteria(ufile)
            return criteria
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error extracting criteria: {str(e)}")


@bonsen_router.post("/score-resumes", response_class=FileResponse)
async def score_resumes(
        criteria: List[str] = Form(...),
        resumes: list[UploadFile] = File(...),
        redis=Depends(get_redis_client)
):
    """
    Endpoint to score resumes based on job description criteria.

    Args:
        criteria (List[str]): A list of criteria extracted from the job description.
        resumes (list[UploadFile]): A list of uploaded resume files.
        redis (Redis): Redis client dependency.

    Returns:
        FileResponse: A CSV file containing the ranked resumes.

    Raises:
        ValueError: If the Redis client is not available or criteria are empty.
    """
    async with AsyncExitStack() as stack:
        redis = await stack.enter_async_context(redis)
        if not redis:
            raise HTTPException(status_code=500, detail="Redis client is not available")
        try:
            evaluator_engine = get_evaluator_engine(redis)
            for cri in criteria:
                if not cri:
                    raise HTTPException(status_code=400, detail="Criteria cannot be empty")
            if len(resumes) > MAX_NUM_FILES:
                raise HTTPException(status_code=400, detail=f"Cannot process more than {MAX_NUM_FILES} files at a time")

            jd_criteria = JDCriteria(criteria=criteria)
            score_file = await evaluator_engine.rank_resumes(jd_criteria, resumes)
            f = FileResponse(score_file.name, media_type="text/csv", filename="results.csv")
            return f
        except ValueError as ve:
            raise HTTPException(status_code=400, detail=f"Exception while scoring resumes {str(ve)}")