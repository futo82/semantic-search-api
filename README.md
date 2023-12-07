# Semantic Search API

This repository is based off of the book "Quick Start Guide to Large Language Models" by Sinan Ozdemir and contains a example of semantic search using OpenAI, Pinecone, and PostgreSQL with the pgvector extension. There are two (2) RESTful endpoints, one to add document into a vector database and the other to query documents from the database.

## Start API Locally

Create a .env file that contains the OPENAI_API_KEY and PINECONE_API_KEY environment variables.

Start the api in the terminal with python.

```
pip install -r requirements.txt

python api.py
```


Start the api in the terminal with docker.
```
docker build -t semantic-search-api .

docker run --env-file ./.env -p 8000:8000 semantic-search-api
```

Pull and run the PostgreSQL docker image with pgvector extension.
``` 
docker pull ankane/pgvector

docker run --name pg-with-pgvector -e POSTGRES_PASSWORD=mysecretpassword -p 5432:5432 -v $HOME/docker/volumes/postgres:/var/lib/postgresql/data ankane/pgvector
```

## API

#### POST /document/add

This endpoint adds a document to the database.

```
curl -X POST \
  http://127.0.0.1:8000/document/add \
  -H 'Content-Type: application/json' \
  -d '{
	"text": "If one assumes that the unit variable cost is constant, as in cost-volume-profit analysis developed and used in cost accounting by the accountants, then total cost is linear in volume, and given by: total cost = fixed costs + unit variable cost * amount."
}'
```

#### POST /documents/retrieve

This endpoint query the database for relevant documents that matches the query.

```
curl -X POST \
  http://127.0.0.1:8000/documents/retrieve \
  -H 'Content-Type: application/json' \
  -d '{
	"query": "is all of thailand in the same time zone"
}'
```

## Dataset

The [BoolQ dataset](https://github.com/google-research-datasets/boolean-questions) was used to build out the semantic search.
