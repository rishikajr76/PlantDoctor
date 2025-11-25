from sqlalchemy import Column, String, Text, JSON, Boolean
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.core.database import Base

class Disease(Base):
    __tablename__ = "diseases"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Disease identification
    name = Column(String(100), unique=True, nullable=False)  # "Tomato_Bacterial_spot"
    scientific_name = Column(String(200))
    common_names = Column(JSON)  # {"en": "Bacterial Spot", "hi": "बैक्टीरियल स्पॉट"}
    
    # Plant information
    plant_type = Column(String(50), nullable=False)  # Tomato, Potato, Pepper, etc.
    affected_parts = Column(JSON)  # ["leaves", "stems", "fruits"]
    
    # Symptoms (multi-language)
    symptoms = Column(JSON)  # {"en": ["Brown spots", "Yellow leaves"], "hi": ["भूरे धब्बे", "पीले पत्ते"]}
    
    # Treatment recommendations (multi-language)
    organic_treatment = Column(JSON)
    chemical_treatment = Column(JSON)
    prevention_tips = Column(JSON)
    
    # Severity information
    is_contagious = Column(Boolean, default=False)
    damage_level = Column(String(20))  # low, medium, high
    
    # Visual references
    example_images = Column(JSON)  # URLs to example images
    seasonal_info = Column(JSON)   # {"common_in": ["rainy", "humid"]}
    
    # Management
    is_active = Column(Boolean, default=True)

    def __repr__(self):
        return f"<Disease(id={self.id}, name={self.name}, plant={self.plant_type})>"