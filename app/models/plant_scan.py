from sqlalchemy import Column, String, DateTime, Float, JSON, ForeignKey, Text, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
from app.core.database import Base

class PlantScan(Base):
    __tablename__ = "plant_scans"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    farmer_id = Column(String(36), ForeignKey("farmers.id"), nullable=False)
    
    # Image information
    image_url = Column(String(500))
    image_filename = Column(String(255))
    
    # Prediction results
    disease_predicted = Column(String(100), nullable=False)
    confidence = Column(Float, nullable=False)  # 0.0 to 1.0
    severity = Column(String(20))  # early, moderate, severe
    
    # Treatment recommendations (multi-language support)
    organic_treatment = Column(JSON)  # {"en": "...", "hi": "...", "te": "..."}
    chemical_treatment = Column(JSON) # {"en": "...", "hi": "...", "te": "..."}
    prevention_tips = Column(JSON)    # {"en": "...", "hi": "...", "te": "..."}
    
    # Additional prediction details
    alternative_diagnoses = Column(JSON)  # [{"disease": "...", "confidence": 0.xx}, ...]
    plant_type = Column(String(50))  # Potato, Tomato, Pepper, etc.
    affected_part = Column(String(50))  # leaf, stem, fruit, etc.
    
    # Image analysis metadata
    image_quality_score = Column(Float)  # 0.0 to 1.0
    analysis_duration = Column(Float)  # seconds taken for prediction
    
    # Farmer feedback
    is_correct_prediction = Column(Boolean, nullable=True)  # True/False/None (not provided)
    farmer_notes = Column(Text)  # Farmer's additional comments
    actual_disease = Column(String(100))  # What farmer says it actually is
    feedback_rating = Column(Float)  # 1-5 stars
    
    # Location and context
    location = Column(String(255))  # GPS coordinates or location name
    weather_conditions = Column(String(100))  # sunny, rainy, humid, etc.
    soil_type = Column(String(50))  # clay, sandy, loamy, etc.
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    feedback_provided_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationship
    farmer = relationship("Farmer", back_populates="scans")

    def to_dict(self):
        """Convert model instance to dictionary for API responses"""
        return {
            "id": self.id,
            "farmer_id": self.farmer_id,
            "image_url": self.image_url,
            "image_filename": self.image_filename,
            "disease_predicted": self.disease_predicted,
            "confidence": self.confidence,
            "severity": self.severity,
            "plant_type": self.plant_type,
            "affected_part": self.affected_part,
            "organic_treatment": self.organic_treatment,
            "chemical_treatment": self.chemical_treatment,
            "prevention_tips": self.prevention_tips,
            "alternative_diagnoses": self.alternative_diagnoses,
            "image_quality_score": self.image_quality_score,
            "analysis_duration": self.analysis_duration,
            "is_correct_prediction": self.is_correct_prediction,
            "farmer_notes": self.farmer_notes,
            "actual_disease": self.actual_disease,
            "feedback_rating": self.feedback_rating,
            "location": self.location,
            "weather_conditions": self.weather_conditions,
            "soil_type": self.soil_type,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "feedback_provided_at": self.feedback_provided_at.isoformat() if self.feedback_provided_at else None
        }

    def __repr__(self):
        return f"<PlantScan(id={self.id}, disease={self.disease_predicted}, confidence={self.confidence:.2f})>"