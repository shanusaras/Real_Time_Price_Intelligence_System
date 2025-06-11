# main.py
from fastapi import FastAPI, HTTPException, Depends, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
import logging
import os
import sys
from pathlib import Path
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

# Import database and models
from api.database import SessionLocal, get_db
from etl.models import Product, PriceHistory

# Initialize FastAPI app
app = FastAPI(
    title="Real Time Price Intelligence System API",
    description="API for accessing product pricing data and analytics",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Welcome to the Real Time Price Intelligence System API",
        "status": "operational",
        "timestamp": datetime.utcnow().isoformat(),
        "endpoints": [
            {"path": "/api/v1/products", "methods": ["GET"], "description": "Get list of products with filters"},
            {"path": "/api/v1/price-history/{product_id}", "methods": ["GET"], "description": "Get price history for a product"}
        ]
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

# Helper function to get latest price for a product
def get_latest_price(db: Session, product_id: int):
    return db.query(PriceHistory)\
        .filter(PriceHistory.product_id == product_id)\
        .order_by(PriceHistory.scraped_at.desc())\
        .first()

# Products endpoint
@app.get("/api/v1/products")
def get_products(
    category: Optional[str] = None,
    brand: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    limit: int = 100,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """
    Get a list of products with optional filtering and pagination
    """
    try:
        # Start building the query
        query = db.query(Product)
        
        # Apply filters
        if category:
            query = query.filter(Product.category.ilike(f"%{category}%"))
        if brand:
            query = query.filter(Product.brand.ilike(f"%{brand}%"))
        
        # Get total count before pagination
        total = query.count()
        
        # Apply pagination
        products = query.offset(offset).limit(limit).all()
        
        # Get latest prices for each product
        results = []
        for product in products:
            latest_price = get_latest_price(db, product.product_id)
            if latest_price:
                results.append({
                    "product_id": product.product_id,
                    "name": product.name,
                    "brand": product.brand,
                    "category": product.category,
                    "price": float(latest_price.price) if latest_price.price else None,
                    "discount_pct": float(latest_price.discount_pct) if latest_price.discount_pct else None,
                    "in_stock": latest_price.in_stock,
                    "rating": latest_price.rating,
                    "reviews": latest_price.reviews,
                    "last_updated": latest_price.scraped_at.isoformat() if latest_price.scraped_at else None,
                    "link": product.link
                })
        
        return {
            "count": len(results),
            "total": total,
            "offset": offset,
            "limit": limit,
            "results": results
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Price history endpoint
@app.get("/api/v1/price-history/{product_id}")
def get_price_history(
    product_id: int,
    days: int = 30,
    db: Session = Depends(get_db)
):
    """
    Get price history for a specific product
    """
    try:
        # Verify product exists
        product = db.query(Product).filter(Product.product_id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        # Calculate date range
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        
        # Get price history
        history = db.query(PriceHistory)\
            .filter(
                PriceHistory.product_id == product_id,
                PriceHistory.scraped_at >= start_date
            )\
            .order_by(PriceHistory.scraped_at.asc())\
            .all()
        
        return {
            "product_id": product_id,
            "product_name": product.name,
            "history": [{
                "price_id": h.price_id,
                "price": float(h.price) if h.price else None,
                "discount_pct": float(h.discount_pct) if h.discount_pct else None,
                "in_stock": h.in_stock,
                "rating": h.rating,
                "reviews": h.reviews,
                "scraped_at": h.scraped_at.isoformat() if h.scraped_at else None
            } for h in history]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)