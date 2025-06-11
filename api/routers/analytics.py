from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from typing import List, Optional
from datetime import datetime, timedelta

from ..database import get_db
from .. import models, schemas

router = APIRouter(
    prefix="/api/v1/analytics",
    tags=["analytics"],
    responses={404: {"description": "Not found"}},
)

@router.get("/summary", response_model=schemas.AnalyticsSummary)
async def get_analytics_summary(db: Session = Depends(get_db)):
    """
    Get key analytics and statistics about the product catalog.
    """
    try:
        # Get total number of products
        total_products = db.query(func.count(models.Product.id)).scalar()
        
        # Get total number of categories
        total_categories = db.query(models.Product.category)\
            .distinct()\
            .count()
        
        # Get average price
        avg_price_result = db.query(func.avg(models.Product.price)).scalar()
        avg_price = float(avg_price_result) if avg_price_result else 0.0
        
        # Get average rating
        avg_rating_result = db.query(func.avg(models.Product.rating)).scalar()
        avg_rating = float(avg_rating_result) if avg_rating_result else None
        
        # Get total reviews
        total_reviews_result = db.query(func.sum(models.Product.review_count)).scalar()
        total_reviews = int(total_reviews_result) if total_reviews_result else 0
        
        # Get last update time
        last_update = db.query(func.max(models.Product.updated_at)).scalar()
        
        return {
            'total_products': total_products,
            'total_categories': total_categories,
            'avg_price': round(avg_price, 2),
            'avg_rating': round(avg_rating, 2) if avg_rating is not None else None,
            'total_reviews': total_reviews,
            'last_updated': last_update or datetime.utcnow()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/categories", response_model=List[schemas.CategoryStats])
async def get_category_stats(db: Session = Depends(get_db)):
    """
    Get statistics for each product category.
    """
    try:
        # Get category statistics using SQLAlchemy core for more complex aggregation
        from sqlalchemy.sql import select, func
        
        stmt = select(
            models.Product.category,
            func.count(models.Product.id).label('product_count'),
            func.min(models.Product.price).label('min_price'),
            func.max(models.Product.price).label('max_price'),
            func.avg(models.Product.price).label('avg_price'),
            func.avg(models.Product.rating).label('avg_rating')
        ).group_by(models.Product.category)
        
        result = db.execute(stmt).all()
        
        return [
            {
                'category': row[0],
                'product_count': row[1],
                'min_price': float(row[2]) if row[2] is not None else 0.0,
                'max_price': float(row[3]) if row[3] is not None else 0.0,
                'avg_price': float(row[4]) if row[4] is not None else 0.0,
                'avg_rating': float(row[5]) if row[5] is not None else None
            }
            for row in result
        ]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/top-rated", response_model=List[schemas.ProductWithPrice])
async def get_top_rated_products(
    limit: int = Query(10, le=100, description="Number of products to return"),
    min_reviews: int = Query(5, description="Minimum number of reviews required"),
    db: Session = Depends(get_db)
):
    """
    Get top rated products with a minimum number of reviews.
    """
    try:
        # Get products with enough reviews, ordered by rating
        products = db.query(models.Product)\
            .filter(models.Product.review_count >= min_reviews)\
            .order_by(models.Product.rating.desc())\
            .limit(limit)\
            .all()
            
        # Convert to response model with latest price
        result = []
        for product in products:
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
                
            result.append(schemas.ProductWithPrice(**product_data))
            
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/price-trends")
async def get_price_trends(
    days: int = Query(30, le=365, description="Number of days to analyze"),
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get price trends over time, optionally filtered by category.
    """
    try:
        from sqlalchemy import text
        
        # Calculate date range
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        
        # Build the query
        query = """
        SELECT 
            DATE(ph.created_at) as date,
            COUNT(DISTINCT ph.product_id) as product_count,
            AVG(ph.price) as avg_price,
            MIN(ph.price) as min_price,
            MAX(ph.price) as max_price
        FROM price_history ph
        JOIN products p ON ph.product_id = p.id
        WHERE ph.created_at BETWEEN :start_date AND :end_date
        """
        
        params = {
            'start_date': start_date,
            'end_date': end_date
        }
        
        if category:
            query += " AND p.category = :category"
            params['category'] = category
            
        query += " GROUP BY DATE(ph.created_at) ORDER BY date"
        
        # Execute raw SQL for complex analytics
        result = db.execute(text(query), params).fetchall()
        
        # Format the response
        return [
            {
                'date': row[0].isoformat(),
                'product_count': row[1],
                'avg_price': float(row[2]) if row[2] else 0.0,
                'min_price': float(row[3]) if row[3] else 0.0,
                'max_price': float(row[4]) if row[4] else 0.0
            }
            for row in result
        ]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
