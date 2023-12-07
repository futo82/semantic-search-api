from pydantic import BaseModel

class InsertRequest(BaseModel):
    text: str

class SearchRequest(BaseModel):
    query: str
    re_ranking_strategy: str = "none"
    num_results: int = 3