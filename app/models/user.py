from sqlalchemy import Column, String, DateTime, Boolean, JSON
from sqlalchemy.sql import func
import uuid
from app.core.database import Base

class Farmer(Base):
    __tablename__ = "farmers"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    phone = Column(String(15), unique=True, nullable=False, index=True)
    name = Column(String(100))
    language = Column(String(10), default="en")  # en, hi, kn, te, ta
    location = Column(JSON)  # Store as {"state": "Karnataka", "district": "Bangalore"}
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<Farmer(id={self.id}, phone={self.phone}, name={self.name})>"