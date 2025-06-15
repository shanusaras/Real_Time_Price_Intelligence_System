"""
Main FastAPI application module for the Price Intelligence System.

This module initializes the FastAPI application, configures middleware,
and includes all API routers.
"""
import logging
from contextlib import asynccontextmanager
from typing import Any, Dict

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.orm import Session

from .config import settings
from .db import get_db, check_database_connection
from .routers import base, category, product, price

# Configure logging
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format=settings.LOG_FORMAT
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for FastAPI app."""
    # Startup: Initialize database
    try:
        logger.info("Starting application...")
        
        # Check database connection
        if not check_database_connection():
            raise RuntimeError("Failed to connect to the database")
            
        logger.info("Application startup complete")
    except Exception as e:
        logger.error(f"Application startup failed: {e}")
        raise
    
    yield
    
    # Shutdown: Clean up resources
    logger.info("Shutting down application...")

# Create FastAPI app with lifespan management
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API for Price Intelligence System",
    version="1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
    lifespan=lifespan
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(GZipMiddleware, minimum_size=1000)  # Compress responses > 1KB

# Include API routers
app.include_router(base.router, prefix=settings.API_V1_STR)
app.include_router(
    category.router, 
    prefix=f"{settings.API_V1_STR}/categories", 
    tags=["categories"]
)
app.include_router(
    product.router, 
    prefix=f"{settings.API_V1_STR}/products", 
    tags=["products"]
)
app.include_router(
    price.router, 
    prefix=f"{settings.API_V1_STR}/prices", 
    tags=["prices"]
)

# Health check endpoint
@app.get("/health")
async def health_check(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """
    Health check endpoint for monitoring.
    
    Returns:
        Dict with status and database connection status
    """
    try:
        # Test database connection
        db.execute(text("SELECT 1"))
        db.commit()
        
        return {
            "status": "healthy",
            "database": "connected",
            "version": "1.0.0"
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "status": "unhealthy",
                "database": "disconnected",
                "error": str(e)
            }
        )

# Root endpoint
@app.get("/", response_model=Dict[str, str])
async def root() -> Dict[str, str]:
    """
    Root endpoint that provides API information.
    
    Returns:
        Welcome message with API information
    """
    return {
        "message": "Welcome to the Price Intelligence System API",
        "version": "1.0.0",
        "docs": f"{settings.API_V1_STR}/docs",
        "redoc": f"{settings.API_V1_STR}/redoc"
    }

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler for uncaught exceptions."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Internal server error",
            "error": str(exc)
        }
    )
