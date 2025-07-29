from typing import List

from pydantic import BaseModel


class JDCriteria(BaseModel):
    criteria: List[str]
