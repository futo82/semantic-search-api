# Semantic Search API

This repository is based off of the book "Quick Start Guide to Large Language Models" by Sinan Ozdemir and contains a example of semantic search using OpenAI, Pinecone, and PostgreSQL with the pgvector extension. You can configure the API to use Pinecone or PostgreSQL vector database. There are two (2) RESTful endpoints, one to add document into a vector database and the other to query documents from the database.

## Start API with Python

Prerequisite: PostgreSQL with the pgvector extension is running on your localhost on port 5432.

Create a .env file that contains the VECTOR_DB, OPENAI_API_KEY, PINECONE_API_KEY, and POSTGRES_URL environment variables.

```
VECTOR_DB=postgres
OPENAI_API_KEY=YOUR_OPEN_AI_API_KEY
PINECONE_API_KEY=YOUR_PINECONE_API_KEY
POSTGRES_URL=postgresql://postgres:mysecretpassword@localhost:5432/postgres
```

Start the API in the terminal with python.

```
pip install -r requirements.txt

python api.py
```

## Start API with Docker

Option 1: Build the API docker image and startup the container. This option assumes you have PostgreSQL with the pgvector extension is running on your localhost on port 5432.

Create a .env file that contains the VECTOR_DB, OPENAI_API_KEY, PINECONE_API_KEY, and POSTGRES_URL environment variables.

```
VECTOR_DB=postgres
OPENAI_API_KEY=YOUR_OPEN_AI_API_KEY
PINECONE_API_KEY=YOUR_PINECONE_API_KEY
POSTGRES_URL=postgresql://postgres:mysecretpassword@localhost:5432/postgres
```

Start the docker API container.
```
docker build -t semantic-search-api .

docker run --env-file ./.env -p 8000:8000 semantic-search-api
```

Option 2: Use docker compose to startup the API and PostgreSQL with the pgvector extension containers. For the database, we use the ankane/pgvector image.

Create a .env file that contains the VECTOR_DB, OPENAI_API_KEY, PINECONE_API_KEY, and POSTGRES_URL environment variables.

```
VECTOR_DB=postgres
OPENAI_API_KEY=YOUR_OPEN_AI_API_KEY
PINECONE_API_KEY=YOUR_PINECONE_API_KEY
POSTGRES_URL=postgresql://postgres:mysecretpassword@db:5432/postgres
```

Start the docker API and database containers.
``` 
docker compose build

docker compose up -d
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
