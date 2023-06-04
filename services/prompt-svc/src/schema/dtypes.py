from pydantic import BaseModel
from typing import List

class RequestModel(BaseModel):
    text: str
    timeout: int 

class ResponseModel(BaseModel):
    result: List[str]