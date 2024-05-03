from database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.sql import func
from pydantic import BaseModel
class Note(Base):
    __tablename__ = 'notes'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150),)
    text = Column(String())
    timestamp = Column(TIMESTAMP(timezone=True), server_default=func.now())

