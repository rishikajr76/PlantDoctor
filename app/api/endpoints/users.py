from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import Farmer
from app.schemas.user import FarmerResponse, FarmerUpdate

router = APIRouter()

@router.get("/me", response_model=FarmerResponse)
async def get_current_user(farmer_id: str = "1", db: Session = Depends(get_db)):
    """
    Get current farmer profile (mock implementation)
    """
    farmer = db.query(Farmer).filter(Farmer.id == farmer_id).first()
    if not farmer:
        raise HTTPException(status_code=404, detail="Farmer not found")
    
    return farmer

@router.put("/me", response_model=FarmerResponse)
async def update_current_user(
    farmer_update: FarmerUpdate, 
    farmer_id: str = "1", 
    db: Session = Depends(get_db)
):
    """
    Update current farmer profile (mock implementation)
    """
    farmer = db.query(Farmer).filter(Farmer.id == farmer_id).first()
    if not farmer:
        raise HTTPException(status_code=404, detail="Farmer not found")
    
    # Update fields if provided
    if farmer_update.name is not None:
        farmer.name = farmer_update.name
    if farmer_update.language is not None:
        farmer.language = farmer_update.language
    if farmer_update.location is not None:
        farmer.location = farmer_update.location
    
    db.commit()
    db.refresh(farmer)
    
    return farmer

@router.get("/{farmer_id}", response_model=FarmerResponse)
async def get_farmer(farmer_id: str, db: Session = Depends(get_db)):
    """
    Get farmer by ID (for development)
    """
    farmer = db.query(Farmer).filter(Farmer.id == farmer_id).first()
    if not farmer:
        raise HTTPException(status_code=404, detail="Farmer not found")
    
    return farmer

@router.get("/")
async def list_farmers(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    List all farmers (for development)
    """
    farmers = db.query(Farmer).offset(skip).limit(limit).all()
    total = db.query(Farmer).count()
    
    return {
        "farmers": farmers,
        "total": total,
        "skip": skip,
        "limit": limit
    }