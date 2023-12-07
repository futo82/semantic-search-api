import os
import pinecone

from dotenv import load_dotenv

load_dotenv()

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

def insert_embedding(id, embedding, metadata):
    if not pinecone_key:
        return False
    pinecone_request = [(id, embedding, metadata)]
    if (index.upsert(pinecone_request).get('upserted_count') != 1):
        return False
    return True

def retrieve_results(query_embedding, num_results, include_metadata=True):
    if not pinecone_key:
        return None
    return index.query(
        vector=query_embedding,
        top_k=num_results,
        include_metadata=include_metadata
    ).get('matches')

    