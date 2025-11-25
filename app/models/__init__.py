# Import all models here so they can be discovered by SQLAlchemy
from app.models.user import Farmer
from app.models.plant_scan import PlantScan
from app.models.disease import Disease

__all__ = ["Farmer", "PlantScan", "Disease"]