from pydantic import BaseModel

class GetCompletionReq(BaseModel):
    model: str
    prompt: str
    max_tokens: int = 1000
    temperature: float = 0.7