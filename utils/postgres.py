import os

from dotenv import load_dotenv
from models.db.models import Document
from sqlmodel import SQLModel, Session, create_engine, select

load_dotenv()

POSTGRES_URL = os.environ.get("POSTGRES_URL")
postgres_engine = create_engine(POSTGRES_URL, echo=True)
SQLModel.metadata.create_all(postgres_engine)

def insert_embedding(hash_value, embedding, metadata):
    doc = Document(
        hash = hash_value,
        embedding = embedding,
        text = metadata["text"]
    )
    session = Session(postgres_engine)
    session.add(doc)
    session.commit()
    return True
    
def retrieve_results(query_embedding, num_results):
    session = Session(postgres_engine)
    docs = session.exec(select(Document).order_by(Document.embedding.cosine_distance(query_embedding)).limit(num_results))
    return docs