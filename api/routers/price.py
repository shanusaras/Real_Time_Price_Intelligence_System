from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta

from ..database import get_db
from ..models import Price as PriceModel, Product as ProductModel
from ..schemas.price import Price, PriceCreate, PriceUpdate
from ..schemas.base import ResponseModel, Message

router = APIRouter(
    prefix="/prices",
    tags=["prices"]
)

@router.post("/", response_model=ResponseModel[Price], status_code=status.HTTP_201_CREATED)
async def create_price(
    price: PriceCreate,
    db: Session = Depends(get_db)
):
    """Create a new price entry"""
    # Check if product exists
    db_product = db.query(ProductModel).filter(ProductModel.id == price.product_id).first()
    if not db_product:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid product ID"
        )
    
    db_price = PriceModel(**price.model_dump())
    db.add(db_price)
    db.commit()
    db.refresh(db_price)
    
    return ResponseModel[Price](
        success=True,
        message="Price entry created successfully",
        data=db_price
    )

@router.get("/{price_id}", response_model=ResponseModel[Price])
async def get_price(
    price_id: int,
    db: Session = Depends(get_db)
):
    """Get a single price entry by ID"""
    db_price = db.query(PriceModel).filter(PriceModel.id == price_id).first()
    if not db_price:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Price entry not found"
        )
    return ResponseModel[Price](
        success=True,
        data=db_price
    )

@router.get("/product/{product_id}/latest", response_model=ResponseModel[Price])
async def get_latest_price(
    product_id: int,
    db: Session = Depends(get_db)
):
    """Get the latest price for a product"""
    # Check if product exists
    if not db.query(ProductModel).filter(ProductModel.id == product_id).first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    latest_price = (
        db.query(PriceModel)
        .filter(PriceModel.product_id == product_id)
        .order_by(PriceModel.created_at.desc())
        .first()
    )
    
    if not latest_price:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No price history found for this product"
        )
    
    return ResponseModel[Price](
        success=True,
        data=latest_price
    )

@router.get("/product/{product_id}/history", response_model=ResponseModel[List[Price]])
async def get_price_history(
    product_id: int,
    days: int = 30,
    db: Session = Depends(get_db)
):
    """Get price history for a product over a time period"""
    # Check if product exists
    if not db.query(ProductModel).filter(ProductModel.id == product_id).first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    # Calculate date threshold
    date_threshold = datetime.utcnow() - timedelta(days=days)
    
    # Get price history
    prices = (
        db.query(PriceModel)
        .filter(
            PriceModel.product_id == product_id,
            PriceModel.created_at >= date_threshold
        )
        .order_by(PriceModel.created_at.desc())
        .all()
    )
    
    return ResponseModel[List[Price]](
        success=True,
        data=prices
    )
