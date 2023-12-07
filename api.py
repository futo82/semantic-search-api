import hashlib
import utils.pinecone
import utils.postgres
import uvicorn

from datetime import datetime
from fastapi import FastAPI, HTTPException,Response, status

from models.schemas.request import InsertRequest, SearchRequest
from models.schemas.response import DocumentResponse, SearchResponse
from numpy import dot
from numpy.linalg import norm
from utils.openai import get_embedding

app = FastAPI()

# Return the MD5 hash of the input string as a hexadecimal string
def hash_str(s):
    return hashlib.md5(s.encode()).hexdigest()

# Calculate the cosine similarity between 2 list
def cosine_similarity(a, b):
    return dot(a, b) / (norm(a) * norm(b))

@app.post("/document/add", status_code=status.HTTP_201_CREATED)
async def add_document(request: InsertRequest, response: Response):
    hash_value = hash_str(request.text)
    embedding = get_embedding(request.text)
    metadata = dict(text=request.text, date_uploaded=datetime.utcnow())

    if (request.db_type == "pinecone"):
        if (not utils.pinecone.insert_embedding(hash_value, embedding, metadata)):
            raise HTTPException(status_code=500, detail="Failed to add document.")
    elif (request.db_type == "postgres"):
        utils.postgres.insert_embedding(hash_value, embedding, metadata)
    else:
        raise HTTPException(status_code=400, detail="Invalid db_type.")

@app.post("/documents/retrieve", response_model=SearchResponse)
async def retrieve_documents(request: SearchRequest):
    query = request.query
    re_ranking_strategy = request.re_ranking_strategy
    query_embedding = get_embedding(query)
    num_results = request.num_results
    include_metadata = True

    results = []
    if (request.db_type == "pinecone"):
        top_results = utils.pinecone.retrieve_results(query_embedding, num_results, include_metadata)
        if top_results is None:
            return SearchResponse(documents=[])

        # Apply the re-rank strategy before returning the results
        if re_ranking_strategy == "none":
            results = top_results
        elif re_ranking_strategy == "date":
            results = sorted(top_results, key=lambda x: x['metadata']['date_uploaded'], reverse=True)
        else:
            raise HTTPException(status_code=400, detail="Invalid re-ranking strategy.")

        results = [
            DocumentResponse
            (
                text=r['metadata']['text'],
                date_uploaded=r['metadata']['date_uploaded'],
                score=r['score'],
                id=r['id']
            ) for r in top_results
        ]
    elif (request.db_type == "postgres"):
        top_results = utils.postgres.retrieve_results(query_embedding, num_results)
        results = [
            DocumentResponse
            (
                text=r.text,
                date_uploaded=r.date_uploaded,
                score=cosine_similarity(query_embedding, r.embedding),
                id=r.hash
            ) for r in top_results
        ]
    else:
        raise HTTPException(status_code=400, detail="Invalid db_type.")

    return SearchResponse(documents=results)

if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)