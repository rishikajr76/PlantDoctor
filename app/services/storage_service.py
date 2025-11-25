import os
import uuid
from typing import Optional
from fastapi import UploadFile
import base64
from io import BytesIO
from PIL import Image

from app.core.config import settings

class StorageService:
    
    @staticmethod
    async def save_image(file: UploadFile, farmer_id: str) -> str:
        """
        Save uploaded image file (mock implementation)
        In production, save to cloud storage (AWS S3, Google Cloud Storage, etc.)
        """
        try:
            # Generate unique filename
            file_extension = file.filename.split('.')[-1] if '.' in file.filename else 'jpg'
            filename = f"{farmer_id}_{uuid.uuid4().hex}.{file_extension}"
            
            # In production, you would:
            # 1. Upload to AWS S3: s3_client.upload_fileobj(...)
            # 2. Upload to Google Cloud Storage: bucket.blob(...).upload_from_file(...)
            # 3. Get public URL
            
            # For now, return mock URL
            mock_url = f"https://storage.plantdoctor.com/images/{filename}"
            
            return mock_url
            
        except Exception as e:
            raise Exception(f"Failed to save image: {str(e)}")
    
    @staticmethod
    async def save_base64_image(image_data: str, farmer_id: str) -> str:
        """
        Save base64 encoded image (for mobile app uploads)
        """
        try:
            # Generate unique filename
            filename = f"{farmer_id}_{uuid.uuid4().hex}.jpg"
            
            # Decode base64 data
            image_bytes = base64.b64decode(image_data)
            
            # Process image (resize, optimize, etc.)
            image = Image.open(BytesIO(image_bytes))
            
            # In production, save to cloud storage
            # For now, return mock URL
            mock_url = f"https://storage.plantdoctor.com/images/{filename}"
            
            return mock_url
            
        except Exception as e:
            raise Exception(f"Failed to save base64 image: {str(e)}")
    
    @staticmethod
    async def delete_image(image_url: str) -> bool:
        """
        Delete image from storage (mock implementation)
        """
        try:
            # In production, delete from cloud storage
            # For now, just return success
            return True
        except Exception as e:
            print(f"Failed to delete image {image_url}: {e}")
            return False
    
    @staticmethod
    def validate_image_file(file: UploadFile) -> bool:
        """
        Validate uploaded image file
        """
        # Check file size
        file.file.seek(0, 2)  # Seek to end
        file_size = file.file.tell()
        file.file.seek(0)  # Reset to beginning
        
        if file_size > settings.MAX_FILE_SIZE:
            return False
        
        # Check content type
        if file.content_type not in settings.ALLOWED_IMAGE_TYPES:
            return False
        
        return True
    
    @staticmethod
    def validate_base64_image(image_data: str) -> bool:
        """
        Validate base64 image data
        """
        try:
            # Check if it's valid base64
            base64.b64decode(image_data)
            return True
        except Exception:
            return False
    
    @staticmethod
    def get_image_info(image_url: str) -> dict:
        """
        Get image information (mock implementation)
        """
        return {
            "url": image_url,
            "size": "2.5MB",  # Mock size
            "format": "JPEG",  # Mock format
            "dimensions": "224x224"  # Mock dimensions
        }

class LocalStorageService:
    """
    Alternative service for local file storage (for development)
    """
    
    @staticmethod
    async def save_image_locally(file: UploadFile, farmer_id: str, upload_dir: str = "uploads") -> str:
        """
        Save image to local filesystem (for development)
        """
        try:
            # Create upload directory if it doesn't exist
            os.makedirs(upload_dir, exist_ok=True)
            
            # Generate unique filename
            file_extension = file.filename.split('.')[-1] if '.' in file.filename else 'jpg'
            filename = f"{farmer_id}_{uuid.uuid4().hex}.{file_extension}"
            file_path = os.path.join(upload_dir, filename)
            
            # Save file
            contents = await file.read()
            with open(file_path, "wb") as f:
                f.write(contents)
            
            # Return relative path
            return f"/{upload_dir}/{filename}"
            
        except Exception as e:
            raise Exception(f"Failed to save image locally: {str(e)}")