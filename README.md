# Semantic Search API

This repository is based off of the book "Quick Start Guide to Large Language Models" by Sinan Ozdemir and contains a simple example of semantic search using OpenAI and Pinecone. There are two (2) RESTful endpoints, one to add document into a vector database and the other to query documents from the database.

## Start API

```
pip install -r requirements.txt
python api.py
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

#### GET /documents/retrieve

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

The [BoolQ dataset](https://github.com/google-research-datasets/boolean-questions) was used to build out the the semantic search.
