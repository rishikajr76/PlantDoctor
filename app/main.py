from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from PIL import Image
import io

# Import database and models
from app.core.database import get_db, create_tables
from app.models.farmer import Farmer
from app.models.plant_scan import PlantScan

app = FastAPI(
    title="Plant Doctor API",
    description="AI-powered plant disease detection",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    create_tables()
    print("✅ Database tables created")

@app.get("/")
async def root():
    return {"message": "🌱 Plant Doctor API is running!"}

@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    try:
        db.execute("SELECT 1")
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}

@app.get("/api/plants/supported")
async def supported_plants():
    return {
        "supported_plants": ["Potato", "Tomato", "Pepper"],
        "status": "Ready for ML model integration"
    }

@app.post("/api/predict/test")
async def test_prediction(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        # Create test record
        test_scan = PlantScan(
            farmer_id="test-farmer-123",
            image_filename=file.filename,
            disease_predicted="Test Disease",
            confidence=0.85,
            plant_type="Tomato"
        )
        
        db.add(test_scan)
        db.commit()
        
        return {
            "success": True,
            "message": "API working! Ready for ML model.",
            "image_size": image.size,
            "scan_id": test_scan.id
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)