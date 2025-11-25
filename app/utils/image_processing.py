import cv2
import numpy as np
from PIL import Image, ImageEnhance
import io
from typing import Tuple, Optional
import logging

logger = logging.getLogger(__name__)

def preprocess_image(image: Image.Image, target_size: Tuple[int, int] = (224, 224)) -> np.ndarray:
    """
    Preprocess image for model prediction.
    
    Args:
        image: PIL Image object
        target_size: Target size for the image (width, height)
    
    Returns:
        Preprocessed numpy array ready for model prediction
    """
    try:
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Resize image
        image = image.resize(target_size, Image.Resampling.LANCZOS)
        
        # Convert to numpy array
        img_array = np.array(image)
        
        # Normalize pixel values to [0, 1]
        img_array = img_array.astype('float32') / 255.0
        
        # Add batch dimension
        img_array = np.expand_dims(img_array, axis=0)
        
        return img_array
        
    except Exception as e:
        logger.error(f"Error preprocessing image: {str(e)}")
        raise ValueError(f"Error preprocessing image: {str(e)}")

def validate_image(image: Image.Image, min_size: Tuple[int, int] = (100, 100)) -> bool:
    """
    Validate if the image is suitable for analysis.
    
    Args:
        image: PIL Image object
        min_size: Minimum allowed dimensions (width, height)
    
    Returns:
        Boolean indicating if image is valid
    """
    try:
        # Check image dimensions
        if image.size[0] < min_size[0] or image.size[1] < min_size[1]:
            return False
        
        # Check if image is not empty
        if image.size[0] == 0 or image.size[1] == 0:
            return False
        
        # Convert to array and check for valid pixel values
        img_array = np.array(image)
        
        # Check if image has valid pixel range
        if img_array.min() == img_array.max():
            return False  # All pixels are the same value
            
        return True
        
    except Exception as e:
        logger.error(f"Error validating image: {str(e)}")
        return False

def enhance_image(image: Image.Image, 
                  contrast_factor: float = 1.2,
                  sharpness_factor: float = 1.1) -> Image.Image:
    """
    Enhance image quality for better analysis.
    
    Args:
        image: PIL Image object
        contrast_factor: Contrast enhancement factor
        sharpness_factor: Sharpness enhancement factor
    
    Returns:
        Enhanced PIL Image
    """
    try:
        # Enhance contrast
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(contrast_factor)
        
        # Enhance sharpness
        enhancer = ImageEnhance.Sharpness(image)
        image = enhancer.enhance(sharpness_factor)
        
        return image
        
    except Exception as e:
        logger.warning(f"Could not enhance image: {str(e)}")
        return image

def convert_to_rgb(image: Image.Image) -> Image.Image:
    """
    Convert image to RGB format if necessary.
    
    Args:
        image: PIL Image object
    
    Returns:
        RGB PIL Image
    """
    if image.mode in ('RGBA', 'LA', 'P'):
        # Create a white background
        background = Image.new('RGB', image.size, (255, 255, 255))
        if image.mode == 'P':
            image = image.convert('RGBA')
        background.paste(image, mask=image.split()[-1] if image.mode == 'RGBA' else None)
        return background
    else:
        return image.convert('RGB')

def get_image_statistics(image: Image.Image) -> dict:
    """
    Get basic statistics about the image.
    
    Args:
        image: PIL Image object
    
    Returns:
        Dictionary containing image statistics
    """
    try:
        img_array = np.array(image)
        
        stats = {
            'dimensions': image.size,
            'mode': image.mode,
            'mean_brightness': float(np.mean(img_array)),
            'std_brightness': float(np.std(img_array)),
            'min_pixel': int(np.min(img_array)),
            'max_pixel': int(np.max(img_array))
        }
        
        return stats
        
    except Exception as e:
        logger.error(f"Error getting image statistics: {str(e)}")
        return {'error': str(e)}