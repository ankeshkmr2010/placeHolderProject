from typing import Annotated

from fastapi import APIRouter, File

bonsen_router = APIRouter()

@bonsen_router.get("/ping")
def ping():
    return {"message": "pong"}

@bonsen_router.post("/extract-criteria")
def extract_criteria(file: Annotated[bytes,File(description="Upload a file to extract criteria")]):
    # Placeholder for criteria extraction logic
    print("file contents:", file.decode('utf-8', errors='ignore'))
    return {" File received": True, "file_size": len(file)}
