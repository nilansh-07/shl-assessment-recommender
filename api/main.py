from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import sys
import os
import logging
import traceback

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Add the parent directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

logger.info(f"Current directory: {current_dir}")
logger.info(f"Parent directory: {parent_dir}")
logger.info(f"Python path: {sys.path}")

try:
    from core.recommender import Recommender, Assessment
    logger.info("Successfully imported Recommender and Assessment")
except ImportError as e:
    logger.error(f"Failed to import core modules: {str(e)}")
    logger.error(traceback.format_exc())
    raise

app = FastAPI(
    title="SHL Assessment Recommendation API",
    description="API for recommending SHL assessments based on job descriptions or queries",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Initialize recommender
try:
    recommender = Recommender()
    logger.info("Recommender initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize recommender: {str(e)}")
    logger.error(traceback.format_exc())
    raise

class RecommendationRequest(BaseModel):
    query: str
    max_results: Optional[int] = 10

class RecommendationResponse(BaseModel):
    recommendations: List[Assessment]

@app.post("/api/recommend", response_model=RecommendationResponse)
async def get_recommendations(request: RecommendationRequest):
    """
    Get assessment recommendations based on a natural language query or job description.
    
    Args:
        request: Contains the query and optional max_results parameter
        
    Returns:
        List of recommended assessments with their details
    """
    try:
        logger.info(f"Received recommendation request for query: {request.query}")
        recommendations = recommender.get_recommendations(
            query=request.query,
            max_results=request.max_results
        )
        logger.info(f"Successfully generated {len(recommendations)} recommendations")
        return RecommendationResponse(recommendations=recommendations)
    except Exception as e:
        logger.error(f"Error processing recommendation request: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail=f"Error processing request: {str(e)}"
        )

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Just check if we can access the assessments
        assessments = recommender.db.assessments
        return {
            "status": "healthy",
            "message": "API server is running",
            "assessments_loaded": len(assessments)
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        logger.error(traceback.format_exc())
        return {
            "status": "unhealthy",
            "error": str(e),
            "traceback": traceback.format_exc()
        } 