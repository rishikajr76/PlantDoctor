import numpy as np
from PIL import Image
import logging
from typing import Dict, Any, List
from app.utils.image_processing import preprocess_image, validate_image, enhance_image, get_image_statistics

logger = logging.getLogger(__name__)

class PlantDiseasePredictor:
    def __init__(self, interpreter, input_details, output_details, class_names: List[str], target_plants: List[str]):
        self.interpreter = interpreter
        self.input_details = input_details
        self.output_details = output_details
        self.class_names = class_names
        self.target_plants = target_plants
        
        # Create plant-specific information
        self.plant_categories = self._categorize_by_plant()
    
    def _categorize_by_plant(self) -> Dict[str, List[str]]:
        """Categorize diseases by plant type"""
        categories = {}
        for plant in self.target_plants:
            categories[plant] = [cls for cls in self.class_names if plant.lower() in cls.lower()]
        return categories
    
    def get_supported_plants(self) -> List[Dict[str, Any]]:
        """Get list of supported plants and their diseases"""
        supported = []
        for plant in self.target_plants:
            diseases = [cls.replace(f"{plant}_", "") for cls in self.class_names 
                       if cls.startswith(plant) and "healthy" not in cls]
            healthy = any(cls for cls in self.class_names 
                         if cls.startswith(plant) and "healthy" in cls)
            
            supported.append({
                "plant_name": plant,
                "diseases_count": len(diseases),
                "diseases": diseases,
                "has_healthy_class": healthy
            })
        return supported
    
    def is_supported_plant(self, predicted_class: str) -> bool:
        """Check if the predicted plant is in our target plants"""
        return any(plant.lower() in predicted_class.lower() for plant in self.target_plants)
    
    def predict(self, image: Image.Image) -> Dict[str, Any]:
        """
        Predict plant disease from image using TFLite model.
        
        Args:
            image: PIL Image object
            
        Returns:
            Dictionary containing prediction results
        """
        try:
            # Validate image
            if not validate_image(image):
                raise ValueError("Invalid image provided for prediction")
            
            # Enhance image for better analysis
            enhanced_image = enhance_image(image)
            
            # Preprocess image - get target size from model input
            input_shape = self.input_details[0]['shape']
            target_size = (input_shape[1], input_shape[2])  # (height, width)
            
            processed_image = preprocess_image(enhanced_image, target_size=target_size)
            
            # Remove batch dimension for TFLite (if needed)
            if processed_image.shape[0] == 1:
                processed_image = processed_image[0]
            
            # Set input tensor
            self.interpreter.set_tensor(self.input_details[0]['index'], processed_image.astype(np.float32))
            
            # Run inference
            self.interpreter.invoke()
            
            # Get prediction results
            output_data = self.interpreter.get_tensor(self.output_details[0]['index'])
            predictions = output_data[0]  # Remove batch dimension
            
            # Process results
            confidence = float(np.max(predictions))
            predicted_class_idx = int(np.argmax(predictions))
            predicted_class = self.class_names[predicted_class_idx]
            
            # Get plant type from prediction
            predicted_plant = next((plant for plant in self.target_plants 
                                  if plant.lower() in predicted_class.lower()), "Unknown")
            
            # Get top 3 predictions (filtered for target plants)
            top_3_indices = np.argsort(predictions)[-3:][::-1]
            top_predictions = [
                {
                    "disease": self.class_names[i],
                    "confidence": float(predictions[i]),
                    "plant": next((p for p in self.target_plants if p.lower() in self.class_names[i].lower()), "Unknown")
                }
                for i in top_3_indices
                if any(p.lower() in self.class_names[i].lower() for p in self.target_plants)
            ]
            
            # If no target plant predictions found, use original top 3
            if not top_predictions:
                top_predictions = [
                    {
                        "disease": self.class_names[i],
                        "confidence": float(predictions[i]),
                        "plant": next((p for p in self.target_plants if p.lower() in self.class_names[i].lower()), "Unknown")
                    }
                    for i in top_3_indices
                ]
            
            return {
                "predicted_disease": predicted_class,
                "predicted_plant": predicted_plant,
                "confidence": confidence,
                "top_predictions": top_predictions,
                "is_healthy": "healthy" in predicted_class.lower(),
                "is_supported_plant": self.is_supported_plant(predicted_class),
                "image_statistics": get_image_statistics(image),
                "model_type": "tflite",
                "supported_plants": self.target_plants
            }
            
        except Exception as e:
            logger.error(f"TFLite prediction error: {str(e)}")
            raise