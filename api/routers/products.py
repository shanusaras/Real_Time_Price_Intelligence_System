from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta

from ..database import get_db
from .. import models, schemas

router = APIRouter(
    prefix="/api/v1/products",
    tags=["products"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=schemas.ProductListResponse)
async def get_products(
    category: Optional[str] = None,
    brand: Optional[str] = None,
    min_price: Optional[float] = Query(None, gt=0),
    max_price: Optional[float] = Query(None, gt=0),
    limit: int = Query(100, le=1000),
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """
    Get a list of products with optional filtering and pagination.
    
    - **category**: Filter by category name
    - **brand**: Filter by brand name
    - **min_price**: Minimum price filter
    - **max_price**: Maximum price filter
    - **limit**: Number of items per page (max 1000)
    - **offset**: Number of items to skip for pagination
    """
    try:
        # Start building the query
        query = db.query(models.Product)
        
        # Apply filters
        if category:
            query = query.filter(models.Product.category.ilike(f"%{category}%"))
        if brand:
            query = query.filter(models.Product.brand.ilike(f"%{brand}%"))
        if min_price is not None:
            query = query.filter(models.Product.price >= min_price)
        if max_price is not None:
            query = query.filter(models.Product.price <= max_price)
        
        # Get total count before pagination
        total = query.count()
        
        # Apply pagination
        products = query.offset(offset).limit(limit).all()
        
        # Convert to Pydantic models
        product_list = []
        for product in products:
            # Get latest price history for each product
            latest_price = db.query(models.PriceHistory)\
                .filter(models.PriceHistory.product_id == product.id)\
                .order_by(models.PriceHistory.created_at.desc())\
                .first()
                
            product_data = product.__dict__
            if latest_price:
                product_data.update({
                    'current_price': latest_price.price,
                    'last_updated': latest_price.created_at
                })
            
            product_list.append(schemas.ProductWithPrice(**product_data))
        
        return {
            'count': len(product_list),
            'total': total,
            'offset': offset,
            'limit': limit,
            'results': product_list
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{product_id}", response_model=schemas.ProductWithPrice)
async def get_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    """
    Get detailed information about a specific product by ID.
    """
    try:
        product = db.query(models.Product).filter(models.Product.id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
            
        # Get latest price history
        latest_price = db.query(models.PriceHistory)\
            .filter(models.PriceHistory.product_id == product_id)\
            .order_by(models.PriceHistory.created_at.desc())\
            .first()
            
        product_data = product.__dict__
        if latest_price:
            product_data.update({
                'current_price': latest_price.price,
                'last_updated': latest_price.created_at
            })
            
        return schemas.ProductWithPrice(**product_data)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{product_id}/price-history", response_model=schemas.PriceHistoryResponse)
async def get_product_price_history(
    product_id: int,
    days: int = Query(30, gt=0, le=365, description="Number of days of history to return"),
    db: Session = Depends(get_db)
):
    """
    Get price history for a specific product.
    
    - **days**: Number of days of price history to return (max 365)
    """
    try:
        # Verify product exists
        product = db.query(models.Product).filter(models.Product.id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        # Calculate date range
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        
        # Get price history
        history = db.query(models.PriceHistory)\
            .filter(
                models.PriceHistory.product_id == product_id,
                models.PriceHistory.created_at >= start_date
            )\
            .order_by(models.PriceHistory.created_at.asc())\
            .all()
            
        return {
            'product_id': product_id,
            'product_name': product.name,
            'history': history
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
