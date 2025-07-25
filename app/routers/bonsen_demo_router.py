from contextlib import AsyncExitStack

from fastapi import APIRouter, UploadFile
from fastapi.params import Depends

from app.interfaces.file_parser import Fileparser
from app.repos.deps import get_file_parser
from app.repos.file_parser.file_parser_impl import FileParserImpl

bonsen_router = APIRouter()




@bonsen_router.get("/ping")
async def ping():
    return {"message": "pong"}

@bonsen_router.post("/extract-criteria")
async def extract_criteria(ufile: UploadFile, file_parser=Depends(get_file_parser)):
    async with AsyncExitStack() as stack:
        file_parser = await stack.enter_async_context(file_parser)
        a =  file_parser.parse_file(ufile)
        return a
