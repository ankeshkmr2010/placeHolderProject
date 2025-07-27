import pytest
from fastapi import UploadFile
from io import BytesIO

from starlette.datastructures import Headers

from app.repos.file_parser.file_parser_impl import FileParserImpl


@pytest.mark.asyncio
async def test_parses_pdf_file_correctly():
    with open("app/tests/Sample.pdf", "rb") as f:
        upload_file = UploadFile(
            file=BytesIO(f.read()),
            filename="samplepdf.pdf",
            headers=Headers({"content-type": "application/pdf"})  # Pass headers as a Headers object
        )
        parser = FileParserImpl()
        result = await parser.parse_file(upload_file)
        result = result.strip().replace("\n", " ")
        assert result == "Ankesh  Kumar", "PDF file content does not match expected output"


@pytest.mark.asyncio
async def test_parses_plain_text_file_correctly():
    pass

@pytest.mark.asyncio
async def test_parses_docx_file_correctly():
    pass

@pytest.mark.asyncio
async def test_raises_error_for_unsupported_file_type():
   pass

@pytest.mark.asyncio
async def test_raises_error_for_missing_file():
    pass

@pytest.mark.asyncio
async def test_raises_error_for_invalid_file_object():
    pass
