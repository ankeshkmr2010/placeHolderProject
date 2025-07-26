from pydantic import BaseModel

class GetCompletionReq(BaseModel):
    model: str
    prompt: str