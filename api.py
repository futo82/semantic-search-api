import hashlib
import os
import pinecone
import uvicorn

from datetime import datetime
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Response, status
from openai import OpenAI
from pydantic import BaseModel

load_dotenv()

client = OpenAI()

# Create an openai client
app = FastAPI()

# Retrieve pinecone api key from environment variable
pinecone_key = os.getenv("PINECONE_API_KEY")
INDEX_NAME = 'semantic-search'

# Create the pinecone index if it does not exist and get a reference to the index.
if pinecone_key:
    pinecone.init(api_key=pinecone_key, environment="gcp-starter")

    if not INDEX_NAME in pinecone.list_indexes():
        pinecone.create_index(
            # The name of the index to create.
            INDEX_NAME,
            # The dimensionality of the vectors that will be indexed.
            dimension=1536,
            # The similarity metric to use when searching the index.
            metric='cosine',
            # The type of Pinecone pod to use for hosting the index.
            pod_type="starter" 
        )
        print('Pinecone index created')
    else:
        print('Pinecone index already exists')

    # Store the index as a variable
    index = pinecone.Index(INDEX_NAME)

# Call openai to create the vector embedding for the text
def get_embedding(text, model="text-embedding-ada-002"):
   text = text.replace("\n", " ")
   return client.embeddings.create(input = [text], model=model).data[0].embedding

# Return the MD5 hash of the input string as a hexadecimal string
def hash_str(s):
    return hashlib.md5(s.encode()).hexdigest()

class InsertRequest(BaseModel):
    text: str

class SearchRequest(BaseModel):
    query: str
    re_ranking_strategy: str = "none"
    num_results: int = 3

class DocumentResponse(BaseModel):
    text: str
    date_uploaded: datetime
    score: float
    id: str

class SearchResponse(BaseModel):
    documents: list

@app.post("/document/add", status_code=status.HTTP_201_CREATED)
async def add_document(request: InsertRequest, response: Response):
    if not pinecone_key:
            raise HTTPException(status_code=500, detail="Failed to initiate database client.")
    
    embedding = get_embedding(request.text)
    pinecone_request = [
        (
            # Generate a unique id for the passage
            hash_str(request.text),
            # The vector embedding of the string
            embedding,
            # A dictionary of metadata
            dict(text=request.text, date_uploaded=datetime.utcnow())
        )
    ]

    if (index.upsert(pinecone_request).get('upserted_count') != 1):
        raise HTTPException(status_code=500, detail="Failed to insert document.")

@app.post("/documents/retrieve", response_model=SearchResponse)
async def retrieve_documents(request: SearchRequest):
    if not pinecone_key:
        return SearchResponse(documents=[])

    query = request.query
    re_ranking_strategy = request.re_ranking_strategy
    query_embedding = get_embedding(query)

    top_results = index.query(
        vector=query_embedding,
        top_k=request.num_results,
        include_metadata=True
    ).get('matches')

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
    return SearchResponse(documents=results)

if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)