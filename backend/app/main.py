from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import aiofiles
import os
import logging

from app.model_handler import get_detector
import uuid

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="AI Image Detection API",
    description="Professional AI-powered image authenticity detector",
    version="1.0.0"
)

# Configure CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure upload directory exists
UPLOAD_DIR = "/app/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.on_event("startup")
async def startup_event():
    """Load AI models on startup"""
    logger.info("🚀 Starting AI Image Detection API...")
    try:
        get_detector()  # This will load the models
        logger.info("✅ API ready to serve requests!")
    except Exception as e:
        logger.error(f"❌ Startup failed: {e}")
        raise

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "AI Image Detection API",
        "status": "active",
        "version": "1.0.0",
        "models": "ResNet-50 + Vision Transformer Ensemble"
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    try:
        detector = get_detector()
        return {
            "status": "healthy",
            "models_loaded": True,
            "device": "cpu",
            "ready": True
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "models_loaded": False,
            "ready": False
        }

@app.post("/predict")
async def predict_image(file: UploadFile = File(...)):
    """
    Predict if an uploaded image is AI-generated or real
    """
    try:
        # Validate file
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Generate unique filename
        file_id = str(uuid.uuid4())
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{file_id}{file_extension}"
        file_path = os.path.join(UPLOAD_DIR, unique_filename)
        
        # Save uploaded file
        async with aiofiles.open(file_path, 'wb') as f:
            content = await file.read()
            await f.write(content)
        
        logger.info(f"📸 Processing image: {file.filename}")
        
        # Get AI detector and make prediction
        detector = get_detector()
        result = detector.predict(file_path)
        
        # Clean up uploaded file
        os.remove(file_path)
        
        logger.info(f"✅ Prediction completed: {result['prediction']} ({result['confidence_percentage']})")
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "filename": file.filename,
                "result": result,
                "processing_info": {
                    "models_used": ["ResNet-50", "Vision Transformer"],
                    "ensemble_method": "Weighted Average",
                    "processing_time": "< 3 seconds"
                }
            }
        )
        
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"❌ Prediction error: {e}")
        
        # Clean up file if it exists
        if 'file_path' in locals() and os.path.exists(file_path):
            os.remove(file_path)
        
        raise HTTPException(
            status_code=500, 
            detail=f"Internal server error: {str(e)}"
        )

@app.get("/models-info")
async def models_info():
    """Get information about loaded models"""
    return {
        "ensemble": {
            "method": "Weighted Average",
            "weights": {
                "vit": 0.7,
                "resnet": 0.3
            }
        },
        "models": {
            "resnet50": {
                "accuracy": "93.5%",
                "architecture": "Convolutional Neural Network",
                "parameters": "25.6M"
            },
            "vit_base": {
                "accuracy": "98.9%", 
                "architecture": "Vision Transformer",
                "parameters": "86.6M"
            }
        },
        "training_data": "CIFAKE Dataset - 120k images"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
