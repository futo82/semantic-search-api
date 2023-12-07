from pydantic import BaseModel

class InsertRequest(BaseModel):
    text: str
    db_type: str = "postgres"

class SearchRequest(BaseModel):
    query: str
    re_ranking_strategy: str = "none"
    num_results: int = 3
    db_type: str = "postgres"