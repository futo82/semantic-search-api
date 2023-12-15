import utils.pinecone
import utils.postgres

from fastapi import HTTPException
from models.schemas.response import DocumentResponse, SearchResponse
from numpy import dot
from numpy.linalg import norm

# Calculate the cosine similarity between 2 list
def cosine_similarity(a, b):
    return dot(a, b) / (norm(a) * norm(b))

class BaseRequestHandler:
    def insert_embedding(self, hash_value, embedding, metadata):
        raise HTTPException(status_code=500, detail="Method not implemented.")

    def retrieve_results(self, query_embedding, num_results, re_ranking_strategy):
        raise HTTPException(status_code=500, detail="Method not implemented.")

class PineconeRequestHandler(BaseRequestHandler):
    def insert_embedding(self, hash_value, embedding, metadata):
        if (not utils.pinecone.insert_embedding(hash_value, embedding, metadata)):
            raise HTTPException(status_code=500, detail="Failed to add document.")

    def retrieve_results(self, query_embedding, num_results, re_ranking_strategy):
        top_results = utils.pinecone.retrieve_results(query_embedding, num_results, True)
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

        return SearchResponse(documents=results)
        

class PostgresRequestHandler(BaseRequestHandler):
    def insert_embedding(self, hash_value, embedding, metadata):
        utils.postgres.insert_embedding(hash_value, embedding, metadata)

    def retrieve_results(self, query_embedding, num_results, re_ranking_strategy):
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
        return SearchResponse(documents=results)