from datetime import datetime
from pydantic import BaseModel

class DocumentResponse(BaseModel):
    text: str
    date_uploaded: datetime
    score: float
    id: str

class SearchResponse(BaseModel):
    documents: list