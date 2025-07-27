# app/models.py

from sqlalchemy import Column, Integer, String, Float, DateTime, func
from app.database import Base

# Gives structure to 'documents' database table
class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String, nullable=False)
    confidence = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())