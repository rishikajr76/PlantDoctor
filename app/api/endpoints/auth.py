from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta

from app.core.database import get_db
from app.core.security import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from app.schemas.user import Token, FarmerCreate, FarmerResponse
from app.models.user import Farmer

router = APIRouter()

# Mock user data for development
MOCK_FARMERS = {
    "1234567890": {"id": "1", "phone": "1234567890", "name": "Test Farmer", "language": "en", "is_verified": True}
}

@router.post("/register", response_model=FarmerResponse)
async def register_farmer(farmer_data: FarmerCreate, db: Session = Depends(get_db)):
    """
    Register a new farmer (mock implementation)
    """
    # Check if farmer already exists
    existing_farmer = db.query(Farmer).filter(Farmer.phone == farmer_data.phone).first()
    if existing_farmer:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Farmer with this phone already exists"
        )
    
    # Create new farmer
    new_farmer = Farmer(
        phone=farmer_data.phone,
        name=farmer_data.name,
        language=farmer_data.language,
        location=farmer_data.location
    )
    
    db.add(new_farmer)
    db.commit()
    db.refresh(new_farmer)
    
    return new_farmer

@router.post("/login", response_model=Token)
async def login(phone: str, db: Session = Depends(get_db)):
    """
    Login farmer (mock implementation - in production, add OTP verification)
    """
    # Find farmer by phone
    farmer = db.query(Farmer).filter(Farmer.phone == phone).first()
    if not farmer:
        # For development, create farmer if not exists
        farmer = Farmer(phone=phone, name="Demo Farmer")
        db.add(farmer)
        db.commit()
        db.refresh(farmer)
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": farmer.id}, 
        expires_delta=access_token_expires
    )
    
    return Token(
        access_token=access_token,
        token_type="bearer"
    )

@router.post("/send-otp")
async def send_otp(phone: str):
    """
    Send OTP to farmer's phone (mock implementation)
    """
    # In production, integrate with SMS service like Twilio, MSG91, etc.
    return {
        "message": "OTP sent successfully", 
        "phone": phone,
        "otp": "123456"  # Mock OTP for development
    }

@router.post("/verify-otp", response_model=Token)
async def verify_otp(phone: str, otp: str, db: Session = Depends(get_db)):
    """
    Verify OTP and login farmer (mock implementation)
    """
    # Mock OTP verification - always succeeds in development
    if otp != "123456":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid OTP"
        )
    
    # Find or create farmer
    farmer = db.query(Farmer).filter(Farmer.phone == phone).first()
    if not farmer:
        farmer = Farmer(phone=phone, name="New Farmer", is_verified=True)
        db.add(farmer)
        db.commit()
        db.refresh(farmer)
    else:
        farmer.is_verified = True
        db.commit()
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": farmer.id}, 
        expires_delta=access_token_expires
    )
    
    return Token(
        access_token=access_token,
        token_type="bearer"
    )