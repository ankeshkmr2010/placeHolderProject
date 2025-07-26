from contextlib import AsyncExitStack

from fastapi import APIRouter, UploadFile
from fastapi.params import Depends


from app.repos.deps import get_file_parser, get_hiring_manager

bonsen_router = APIRouter()

@bonsen_router.get("/ping")
async def ping():
    return {"message": "pong"}

@bonsen_router.post("/parse-file")
async def parse_input(ufile: UploadFile, file_parser=Depends(get_file_parser)):
    async with AsyncExitStack() as stack:
        file_parser = await stack.enter_async_context(file_parser)
        a = await file_parser.parse_file(ufile)
        return {"file_content": a}


@bonsen_router.post("/extract-criteria")
async def extract_criteria(ufile: UploadFile, hiring_processor=Depends(get_hiring_manager)):
    async with AsyncExitStack() as stack:
        hiring_processor = await stack.enter_async_context(hiring_processor)
        criteria = await hiring_processor.extract_jd_criteria(ufile)
        return criteria
