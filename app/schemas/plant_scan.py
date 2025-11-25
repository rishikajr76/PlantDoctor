from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class PlantScanBase(BaseModel):
    disease_predicted: str
    confidence: float
    severity: str
    organic_treatment: Optional[Dict[str, Any]] = None
    chemical_treatment: Optional[Dict[str, Any]] = None

class PlantScanCreate(PlantScanBase):
    farmer_id: str
    image_url: Optional[str] = None

class PlantScanResponse(PlantScanBase):
    id: str
    farmer_id: str
    image_url: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

class PredictionRequest(BaseModel):
    image_data: str
    language: str = "en"