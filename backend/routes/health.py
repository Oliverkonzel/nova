"""
Health Check Routes
"""
from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Nova Voice Agent",
        "message": "🚀 Server is running!"
    }

@router.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Nova Voice Agent API",
        "endpoints": {
            "health": "/health",
            "webhooks": "/webhooks/voice/*"
        }
    }
