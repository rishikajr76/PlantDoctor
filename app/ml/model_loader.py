import os
import json
import logging
import numpy as np
import tensorflow as tf
from .predictor import PlantDiseasePredictor

logger = logging.getLogger(__name__)

class ModelLoader:
    def __init__(self):
        self.interpreter = None
        self.input_details = None
        self.output_details = None
        self.predictor = None
        self.class_names = []
        self.target_plants = ['Potato', 'Tomato', 'Pepper']  # Your target plants
        
    def load_model(self, model_path: str = None, class_names_path: str = None):
        """Load the TFLite model and class names"""
        try:
            # Set default paths if not provided
            if model_path is None:
                model_path = os.path.join(
                    os.path.dirname(__file__), 
                    'models/plant_disease_model.tflite'
                )
            
            if class_names_path is None:
                class_names_path = os.path.join(
                    os.path.dirname(__file__), 
                    'models/class_names.json'
                )
            
            # Load TFLite model
            logger.info(f"Loading TFLite model from: {model_path}")
            self.interpreter = tf.lite.Interpreter(model_path=model_path)
            self.interpreter.allocate_tensors()
            
            # Get input and output tensors
            self.input_details = self.interpreter.get_input_details()
            self.output_details = self.interpreter.get_output_details()
            
            logger.info(f"Input details: {self.input_details[0]}")
            logger.info(f"Output details: {self.output_details[0]}")
            
            # Load class names
            if os.path.exists(class_names_path):
                with open(class_names_path, 'r') as f:
                    self.class_names = json.load(f)
                logger.info(f"Loaded {len(self.class_names)} class names for {len(self.target_plants)} target plants")
            else:
                # Fallback to your specific plant classes
                self.class_names = [
                    "Pepper_bell_Bacterial_spot", "Pepper_bell_healthy",
                    "Potato_Early_blight", "Potato_Late_blight", "Potato_healthy",
                    "Tomato_Bacterial_spot", "Tomato_Early_blight", "Tomato_Late_blight",
                    "Tomato_Leaf_Mold", "Tomato_Septoria_leaf_spot", "Tomato_Spider_mites",
                    "Tomato_Target_Spot", "Tomato_Yellow_Leaf_Curl_Virus", "Tomato_mosaic_virus",
                    "Tomato_healthy"
                ]
                logger.warning("Class names file not found, using default names for Potato, Tomato, Pepper")
            
            # Initialize predictor
            self.predictor = PlantDiseasePredictor(
                interpreter=self.interpreter,
                input_details=self.input_details,
                output_details=self.output_details,
                class_names=self.class_names,
                target_plants=self.target_plants
            )
            
            logger.info("TFLite model loaded successfully")
            
        except Exception as e:
            logger.error(f"Error loading TFLite model: {str(e)}")
            raise

# Global instance
_model_loader = ModelLoader()

def get_predictor():
    """Dependency function to get the predictor instance"""
    if _model_loader.predictor is None:
        _model_loader.load_model()
    return _model_loader.predictor

def initialize_models():
    """Initialize models on application startup"""
    _model_loader.load_model()