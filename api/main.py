import os
print("DEBUG: Current working directory =", os.getcwd())
print("DEBUG: .env exists =", os.path.isfile('.env'))

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Query, HTTPException
from typing import Optional
from datetime import datetime
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'etl'))
from models import Product, PriceHistory, SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import and_

app = FastAPI(title="Price Intelligence API")

@app.get('/')
def root():
    return {"message": "API running"}

@app.get('/products')
def get_products(
    category: Optional[str] = Query(None, description='Filter by category'),
    brand: Optional[str] = Query(None, description='Filter by brand'),
    min_price: Optional[float] = Query(None, description='Minimum price'),
    max_price: Optional[float] = Query(None, description='Maximum price'),
    limit: int = Query(100, ge=1, le=1000, description='Max number of results')
):
    """Fetch products with optional filters from MySQL"""
    session: Session = SessionLocal()
    try:
        query = session.query(Product)
        filters = []
        if category:
            filters.append(Product.category == category)
        if brand:
            filters.append(Product.brand == brand)
        if min_price is not None or max_price is not None:
            query = query.join(PriceHistory)
            if min_price is not None:
                filters.append(PriceHistory.price >= min_price)
            if max_price is not None:
                filters.append(PriceHistory.price <= max_price)
        if filters:
            query = query.filter(and_(*filters))
        products = query.limit(limit).all()
        # Serialize results
        def serialize_product(p):
            return {
                'product_id': p.product_id,
                'name': p.name,
                'brand': p.brand,
                'category': p.category,
                'link': p.link,
                'created_at': str(p.created_at),
                'updated_at': str(p.updated_at)
            }
        return [serialize_product(p) for p in products]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()

from datetime import datetime
from fastapi import Query

@app.get('/price-history')
def get_price_history(
    product_id: Optional[int] = Query(None, description='Product ID to fetch price history for'),
    product_name: Optional[str] = Query(None, description='Product name to fetch price history for (used only if product_id is not provided)'),
    start_date: Optional[datetime] = Query(None, description='Start date (ISO 8601)'),
    end_date: Optional[datetime] = Query(None, description='End date (ISO 8601)'),
    limit: int = Query(1000, ge=1, le=5000, description='Max number of records to return')
):
    """Fetch price history for a product by product_id (preferred) or product_name (optional)."""
    session = SessionLocal()
    try:
        pid = product_id
        if pid is None:
            if not product_name:
                raise HTTPException(status_code=400, detail="Either product_id or product_name must be provided.")
            product = session.query(Product).filter(Product.name == product_name).first()
            if not product:
                raise HTTPException(status_code=404, detail=f"Product with name '{product_name}' not found.")
            pid = product.product_id
        query = session.query(PriceHistory).filter(PriceHistory.product_id == pid)
        if start_date:
            query = query.filter(PriceHistory.scraped_at >= start_date)
        if end_date:
            query = query.filter(PriceHistory.scraped_at <= end_date)
        query = query.order_by(PriceHistory.scraped_at.desc()).limit(limit)
        results = query.all()
        return [
            {
                'price_id': ph.price_id,
                'product_id': ph.product_id,
                'price': float(ph.price),
                'discount_pct': float(ph.discount_pct) if ph.discount_pct is not None else None,
                'in_stock': ph.in_stock,
                'rating': ph.rating,
                'reviews': ph.reviews,
                'scraped_at': ph.scraped_at.isoformat() if ph.scraped_at else None
            }
            for ph in results
        ]
    finally:
        session.close()


@app.get('/categories')
def get_categories():
    """List all categories with product count and price stats."""
    session = SessionLocal()
    try:
        from sqlalchemy import func
        # Join products and price_history to get stats
        results = (
            session.query(
                Product.category,
                func.count(Product.product_id).label('product_count'),
                func.avg(PriceHistory.price).label('avg_price'),
                func.min(PriceHistory.price).label('min_price'),
                func.max(PriceHistory.price).label('max_price')
            )
            .join(PriceHistory, PriceHistory.product_id == Product.product_id)
            .group_by(Product.category)
            .order_by(Product.category)
            .all()
        )
        categories = [
            {
                'category': row.category,
                'product_count': row.product_count,
                'avg_price': float(row.avg_price) if row.avg_price is not None else None,
                'min_price': float(row.min_price) if row.min_price is not None else None,
                'max_price': float(row.max_price) if row.max_price is not None else None
            }
            for row in results
        ]
        return categories
    finally:
        session.close()

@app.get('/top-rated')
def get_top_rated(limit: int = 20, category: Optional[str] = None):
    """List products with the highest ratings (latest record per product)."""
    session = SessionLocal()
    try:
        from sqlalchemy import func
        subq = (
            session.query(
                PriceHistory.product_id,
                func.max(PriceHistory.scraped_at).label('latest_scraped_at')
            )
            .group_by(PriceHistory.product_id)
            .subquery()
        )
        query = (
            session.query(Product, PriceHistory)
            .join(PriceHistory, Product.product_id == PriceHistory.product_id)
            .join(subq, (PriceHistory.product_id == subq.c.product_id) & (PriceHistory.scraped_at == subq.c.latest_scraped_at))
        )
        if category:
            query = query.filter(Product.category == category)
        query = query.order_by(PriceHistory.rating.desc(), PriceHistory.reviews.desc()).limit(limit)
        results = query.all()
        top_rated = [
            {
                'product_id': p.product_id,
                'name': p.name,
                'category': p.category,
                'rating': ph.rating,
                'reviews': ph.reviews,
                'price': float(ph.price) if ph.price is not None else None,
                'scraped_at': ph.scraped_at.isoformat() if ph.scraped_at else None
            }
            for p, ph in results
        ]
        return top_rated
    finally:
        session.close()


@app.get('/most-reviewed')
def get_most_reviewed(limit: int = 20, category: Optional[str] = None):
    """List products with the most reviews (latest record per product, deduplicated)."""
    session = SessionLocal()
    try:
        from sqlalchemy import func
        subq = (
            session.query(
                PriceHistory.product_id,
                func.max(PriceHistory.scraped_at).label('latest_scraped_at')
            )
            .group_by(PriceHistory.product_id)
            .subquery()
        )
        query = (
            session.query(Product, PriceHistory)
            .join(PriceHistory, Product.product_id == PriceHistory.product_id)
            .join(subq, (PriceHistory.product_id == subq.c.product_id) & (PriceHistory.scraped_at == subq.c.latest_scraped_at))
        )
        if category:
            query = query.filter(Product.category == category)
        query = query.order_by(PriceHistory.reviews.desc(), PriceHistory.rating.desc()).limit(limit * 2)
        results = query.all()
        unique = {}
        for p, ph in results:
            if p.product_id not in unique:
                unique[p.product_id] = {
                    'product_id': p.product_id,
                    'name': p.name,
                    'category': p.category,
                    'reviews': ph.reviews,
                    'rating': ph.rating,
                    'price': float(ph.price) if ph.price is not None else None,
                    'scraped_at': ph.scraped_at.isoformat() if ph.scraped_at else None
                }
        most_reviewed = list(unique.values())[:limit]
        return most_reviewed
    finally:
        session.close()


@app.get('/analytics/summary')
def analytics_summary():
    """Return key performance indicators (KPIs) for the catalog (latest record per product)."""
    session = SessionLocal()
    try:
        from sqlalchemy import func
        subq = (
            session.query(
                PriceHistory.product_id,
                func.max(PriceHistory.scraped_at).label('latest_scraped_at')
            )
            .group_by(PriceHistory.product_id)
            .subquery()
        )
        query = (
            session.query(Product, PriceHistory)
            .join(PriceHistory, Product.product_id == PriceHistory.product_id)
            .join(subq, (PriceHistory.product_id == subq.c.product_id) & (PriceHistory.scraped_at == subq.c.latest_scraped_at))
        )
        results = query.all()
        total_products = 0
        total_reviews = 0
        total_rating = 0.0
        total_price = 0.0
        categories = set()
        for p, ph in results:
            total_products += 1
            total_reviews += ph.reviews or 0
            total_rating += ph.rating or 0.0
            total_price += float(ph.price) if ph.price is not None else 0.0
            if p.category:
                categories.add(p.category)
        avg_rating = total_rating / total_products if total_products else 0.0
        avg_price = total_price / total_products if total_products else 0.0
        return {
            'total_products': total_products,
            'total_categories': len(categories),
            'average_price': round(avg_price, 2),
            'average_rating': round(avg_rating, 2),
            'total_reviews': total_reviews
        }
    finally:
        session.close()

