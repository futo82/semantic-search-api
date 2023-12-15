import hashlib
import os
import uvicorn

from datetime import datetime
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Response, status
from handler import PostgresRequestHandler, PineconeRequestHandler

from models.schemas.request import InsertRequest, SearchRequest
from models.schemas.response import SearchResponse
from utils.openai import get_embedding

load_dotenv()

VECTOR_DB = os.getenv("VECTOR_DB")

app = FastAPI()

# Return the MD5 hash of the input string as a hexadecimal string
def hash_str(s):
    return hashlib.md5(s.encode()).hexdigest()

def create_request_handler():
    print(VECTOR_DB)
    if VECTOR_DB == "postgres":
        return PostgresRequestHandler()
    elif VECTOR_DB == "pinecone":
        return PineconeRequestHandler()
    else:
        raise HTTPException(status_code=500, detail="Environment variable missing or invalid.")

@app.post("/document/add", status_code=status.HTTP_201_CREATED)
async def add_document(request: InsertRequest, response: Response):
    hash_value = hash_str(request.text)
    embedding = get_embedding(request.text)
    metadata = dict(text=request.text, date_uploaded=datetime.utcnow())
    create_request_handler().insert_embedding(
        hash_value, 
        embedding, 
        metadata
    )

@app.post("/documents/retrieve", response_model=SearchResponse)
async def retrieve_documents(request: SearchRequest):
    query = request.query
    re_ranking_strategy = request.re_ranking_strategy
    query_embedding = get_embedding(query)
    num_results = request.num_results
    return create_request_handler().retrieve_results(
        query_embedding,
        num_results,
        re_ranking_strategy
    )

if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)