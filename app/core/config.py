import os
from pydantic import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # API Configuration
    PROJECT_NAME: str = "AI Plant Doctor API"
    DESCRIPTION: str = "🌱 Backend API for Plant Disease Detection Mobile App"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    RELOAD: bool = True
    
    # Database Configuration
    DATABASE_URL: str = "sqlite:///./plant_doctor.db"
    
    # Security Configuration
    SECRET_KEY: str = "your-super-secret-key-change-this-in-production-2024"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # CORS Configuration
    CORS_ORIGINS: list = ["*"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: list = ["*"]
    CORS_ALLOW_HEADERS: list = ["*"]
    
    # ML Model Configuration
    ML_MODEL_PATH: str = "app/ml/models/plant_model.h5"
    ML_MODEL_INPUT_SIZE: tuple = (224, 224)
    ML_MODEL_CLASSES: list = [
        'Tomato_Bacterial_spot', 'Potato___Early_blight', 'Pepper__bell___Bacterial_spot',
        'Potato___healthy', 'Tomato_Early_blight', 'Tomato_Spider_mites_Two_spotted_spider_mite',
        'Tomato_Septoria_leaf_spot', 'Potato___Late_blight', 'Tomato__Tomato_YellowLeaf__Curl_Virus',
        'Pepper__bell___healthy', 'Tomato_healthy', 'Tomato_Late_blight',
        'Tomato_Leaf_Mold', 'Tomato_Target_Spot', 'Tomato_mosaic_virus'
    ]
    
    # File Upload Configuration
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_IMAGE_TYPES: list = ["image/jpeg", "image/png", "image/jpg"]
    
    # SMS Service Configuration (for OTP)
    SMS_PROVIDER: str = "mock"  # mock, twilio, msg91
    TWILIO_ACCOUNT_SID: Optional[str] = None
    TWILIO_AUTH_TOKEN: Optional[str] = None
    TWILIO_PHONE_NUMBER: Optional[str] = None
    MSG91_AUTH_KEY: Optional[str] = None
    
    # Cloud Storage Configuration
    STORAGE_PROVIDER: str = "local"  # local, aws, google
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_S3_BUCKET: Optional[str] = None
    AWS_REGION: Optional[str] = "ap-south-1"
    
    class Config:
        case_sensitive = True
        env_file = ".env"

# Global settings instance
settings = Settings()