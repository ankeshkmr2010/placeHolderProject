from pydantic import BaseModel


class DataRequest(BaseModel):
    text:str