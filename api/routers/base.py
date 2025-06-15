from fastapi import APIRouter
from ..config import settings
from ..schemas.base import ResponseModel, Message

router = APIRouter(
    prefix=settings.API_V1_STR,
    tags=["base"]
)

@router.get("/health", response_model=ResponseModel[dict])
async def health_check():
    """Health check endpoint"""
    return ResponseModel[dict](
        success=True,
        message="Service is healthy",
        data={"status": "ok"}
    )

@router.get("/info", response_model=ResponseModel[dict])
async def api_info():
    """Get API information"""
    return ResponseModel[dict](
        success=True,
        data={
            "name": settings.PROJECT_NAME,
            "version": "1.0.0",
            "docs": "/docs",
            "redoc": "/redoc",
            "openapi": "/openapi.json"
        }
    )
