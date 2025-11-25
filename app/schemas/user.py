from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class FarmerBase(BaseModel):
    phone: str
    name: Optional[str] = None
    language: str = "en"
    location: Optional[Dict[str, Any]] = None

class FarmerCreate(FarmerBase):
    pass

class FarmerUpdate(BaseModel):
    name: Optional[str] = None
    language: Optional[str] = None
    location: Optional[Dict[str, Any]] = None

class FarmerResponse(FarmerBase):
    id: str
    is_verified: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str