from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import uuid
from typing import Optional, Dict, Any

from app.models.user import Farmer
from app.core.security import verify_password, get_password_hash, generate_otp, validate_phone_number
from app.schemas.user import FarmerCreate, FarmerUpdate

class AuthService:
    
    @staticmethod
    def create_farmer(db: Session, farmer_data: FarmerCreate) -> Farmer:
        """
        Create a new farmer account
        """
        # Validate phone number
        if not validate_phone_number(farmer_data.phone):
            raise ValueError("Invalid phone number format")
        
        # Check if farmer already exists
        existing_farmer = db.query(Farmer).filter(Farmer.phone == farmer_data.phone).first()
        if existing_farmer:
            raise ValueError("Farmer with this phone number already exists")
        
        # Create new farmer
        farmer = Farmer(
            phone=farmer_data.phone,
            name=farmer_data.name,
            language=farmer_data.language,
            location=farmer_data.location
        )
        
        db.add(farmer)
        db.commit()
        db.refresh(farmer)
        
        return farmer
    
    @staticmethod
    def get_farmer_by_phone(db: Session, phone: str) -> Optional[Farmer]:
        """
        Get farmer by phone number
        """
        return db.query(Farmer).filter(Farmer.phone == phone).first()
    
    @staticmethod
    def get_farmer_by_id(db: Session, farmer_id: str) -> Optional[Farmer]:
        """
        Get farmer by ID
        """
        return db.query(Farmer).filter(Farmer.id == farmer_id).first()
    
    @staticmethod
    def update_farmer(db: Session, farmer_id: str, update_data: FarmerUpdate) -> Farmer:
        """
        Update farmer profile
        """
        farmer = db.query(Farmer).filter(Farmer.id == farmer_id).first()
        if not farmer:
            raise ValueError("Farmer not found")
        
        # Update fields if provided
        update_dict = update_data.dict(exclude_unset=True)
        for field, value in update_dict.items():
            setattr(farmer, field, value)
        
        db.commit()
        db.refresh(farmer)
        
        return farmer
    
    @staticmethod
    def verify_farmer(db: Session, farmer_id: str) -> Farmer:
        """
        Mark farmer as verified
        """
        farmer = db.query(Farmer).filter(Farmer.id == farmer_id).first()
        if not farmer:
            raise ValueError("Farmer not found")
        
        farmer.is_verified = True
        db.commit()
        db.refresh(farmer)
        
        return farmer
    
    @staticmethod
    def get_or_create_farmer(db: Session, phone: str, name: Optional[str] = None) -> Farmer:
        """
        Get existing farmer or create new one (for OTP login)
        """
        farmer = db.query(Farmer).filter(Farmer.phone == phone).first()
        
        if not farmer:
            # Create new farmer
            farmer = Farmer(
                phone=phone,
                name=name or "New Farmer",
                is_verified=True
            )
            db.add(farmer)
            db.commit()
            db.refresh(farmer)
        else:
            # Mark existing farmer as verified
            farmer.is_verified = True
            db.commit()
        
        return farmer

class OTPService:
    
    @staticmethod
    def generate_otp_record(phone: str) -> Dict[str, Any]:
        """
        Generate OTP and return record (mock implementation)
        In production, store in database with expiration
        """
        otp_code = generate_otp()
        
        return {
            "phone": phone,
            "otp_code": otp_code,
            "expires_at": datetime.utcnow() + timedelta(minutes=10),
            "attempts": 0
        }
    
    @staticmethod
    def verify_otp(phone: str, otp_code: str, stored_otp_record: Dict[str, Any]) -> bool:
        """
        Verify OTP (mock implementation)
        In production, verify against database record
        """
        # Mock verification - always returns True for "123456"
        if otp_code == "123456":
            return True
        
        # In production, you would:
        # 1. Check if OTP exists and not expired
        # 2. Check if attempts < max_attempts
        # 3. Verify OTP code matches
        # 4. Increment attempts if wrong
        
        return False
    
    @staticmethod
    def send_otp_sms(phone: str, otp_code: str) -> bool:
        """
        Send OTP via SMS (mock implementation)
        In production, integrate with SMS provider like Twilio, MSG91, etc.
        """
        try:
            # Mock SMS sending
            print(f"📱 OTP {otp_code} sent to {phone}")
            
            # In production, you would:
            # 1. Use Twilio: client.messages.create(...)
            # 2. Use MSG91: requests.post(...)
            # 3. Handle errors and retries
            
            return True
        except Exception as e:
            print(f"Failed to send OTP: {e}")
            return False