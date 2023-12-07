from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class DocumentResponse(BaseModel):
    text: str
    date_uploaded: datetime
    score: Optional[float] = None
    id: str

class SearchResponse(BaseModel):
    documents: list