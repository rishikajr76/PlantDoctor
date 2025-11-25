from sqlalchemy import Column, String, DateTime, Boolean, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
from app.core.database import Base

class Farmer(Base):
    __tablename__ = "farmers"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True)
    phone = Column(String(20))
    language = Column(String(10), default="en")
    
    # Location information
    farm_location = Column(String(255))
    farm_size = Column(String(50))
    primary_crops = Column(JSON)
    
    # Authentication
    hashed_password = Column(String(255))
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    scans = relationship("PlantScan", back_populates="farmer")

    def __repr__(self):
        return f"<Farmer(id={self.id}, name={self.name})>"