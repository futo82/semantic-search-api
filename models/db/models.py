import datetime

from pgvector.sqlalchemy import Vector
from sqlalchemy import Column
from sqlmodel import Field, SQLModel
from typing import Optional, List

class Document(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True) 
    hash: str
    embedding: List[float] = Field(sa_column=Column(Vector(1536)))
    text: str
    date_uploaded: datetime.datetime = Field(default_factory=datetime.datetime.utcnow, nullable=False)
