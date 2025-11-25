from PIL import Image
from typing import Dict, Any, List
import logging
from app.ml.predictor import PlantDiseasePredictor
from app.utils.image_processing import validate_image

logger = logging.getLogger(__name__)

class PredictionService:
    def __init__(self, predictor: PlantDiseasePredictor):
        self.predictor = predictor
    
    async def predict_disease(self, image: Image.Image, user_id: int = None) -> Dict[str, Any]:
        """Predict plant disease from image"""
        try:
            if not validate_image(image):
                raise ValueError("Invalid image format or quality")
            
            result = self.predictor.predict(image)
            
            if user_id:
                result["user_id"] = user_id
            
            logger.info(f"Prediction completed: {result['predicted_disease']}")
            return result
            
        except Exception as e:
            logger.error(f"Prediction service error: {str(e)}")
            raise
    
    def get_supported_plants(self) -> List[Dict[str, Any]]:
        """Get list of supported plants and their diseases"""
        return self.predictor.get_supported_plants()