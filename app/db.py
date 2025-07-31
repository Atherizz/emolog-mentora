from sqlmodel import SQLModel, create_engine, Session

from typing import Optional, List
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship


mysql_url = "mysql+pymysql://root@localhost/mentora"

engine = create_engine(mysql_url, echo=True)


class EmologHistories(SQLModel, table=True):
    __tablename__ = "emolog_histories" 
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(index=True)
    region_id: int = Field(index=True, foreign_key="regions.id")
    emotion: str = Field(index=True)  
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    

class Regions(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    type: str 
    external_id: str  
    parent_id: Optional[int] = Field(default=None, foreign_key="regions.id")

    children: List["Regions"] = Relationship(back_populates="parent", sa_relationship_kwargs={"cascade": "all, delete"})
    parent: Optional["Regions"] = Relationship(back_populates="children")
 

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
        
