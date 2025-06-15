from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from ..database import get_db
from ..models import Product as ProductModel, Price as PriceModel, Category as CategoryModel
from ..schemas.product import Product, ProductCreate, ProductUpdate
from ..schemas.price import Price
from ..schemas.base import ResponseModel, Message

router = APIRouter(
    prefix="/products",
    tags=["products"]
)

@router.get("/", response_model=ResponseModel[List[Product]])
async def list_products(
    skip: int = 0, 
    limit: int = 100,
    category_id: Optional[int] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    in_stock: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """List products with optional filtering"""
    query = db.query(ProductModel)
    
    # Apply filters
    if category_id is not None:
        query = query.filter(ProductModel.category_id == category_id)
        
    if min_price is not None or max_price is not None or in_stock is not None:
        # Subquery to get latest price for each product
        from sqlalchemy import func
        latest_prices = db.query(
            PriceModel.product_id,
            func.max(PriceModel.created_at).label('latest_time')
        ).group_by(PriceModel.product_id).subquery()
        
        query = query.join(
            latest_prices,
            ProductModel.id == latest_prices.c.product_id
        ).join(
            PriceModel,
            (PriceModel.product_id == latest_prices.c.product_id) & 
            (PriceModel.created_at == latest_prices.c.latest_time)
        )
        
        if min_price is not None:
            query = query.filter(PriceModel.price >= min_price)
        if max_price is not None:
            query = query.filter(PriceModel.price <= max_price)
        if in_stock is not None:
            if in_stock:
                query = query.filter(PriceModel.in_stock > 0)
            else:
                query = query.filter(PriceModel.in_stock <= 0)
    
    products = query.offset(skip).limit(limit).all()
    return ResponseModel[List[Product]](
        success=True,
        data=products
    )

@router.post("/", response_model=ResponseModel[Product], status_code=status.HTTP_201_CREATED)
async def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db)
):
    """Create a new product"""
    # Check if category exists
    if product.category_id is not None:
        category = db.query(CategoryModel).filter(CategoryModel.id == product.category_id).first()
        if not category:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Category with id {product.category_id} does not exist"
            )
    
    # Create product
    db_product = ProductModel(**product.model_dump(exclude={"price", "original_price", "discount", "in_stock"}))
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    
    # Create initial price entry
    db_price = PriceModel(
        product_id=db_product.id,
        price=product.price,
        original_price=product.original_price,
        in_stock=product.in_stock if product.in_stock is not None else 0,
        discount=product.discount if product.discount is not None else 0
    )
    db.add(db_price)
    db.commit()
    db.refresh(db_product)
    
    return ResponseModel[Product](
        success=True,
        message="Product created successfully",
        data=db_product
    )

@router.get("/{product_id}", response_model=ResponseModel[Product])
async def get_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    """Get a single product by ID"""
    db_product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if not db_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return ResponseModel[Product](
        success=True,
        data=db_product
    )

@router.put("/{product_id}", response_model=ResponseModel[Product])
async def update_product(
    product_id: int,
    product: ProductUpdate,
    db: Session = Depends(get_db)
):
    """Update a product"""
    db_product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if not db_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    # Check if category exists if being updated
    if product.category_id is not None and product.category_id != db_product.category_id:
        category = db.query(CategoryModel).filter(CategoryModel.id == product.category_id).first()
        if not category:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Category with id {product.category_id} does not exist"
            )
    
    update_data = product.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_product, field, value)
    
    db.commit()
    db.refresh(db_product)
    
    return ResponseModel[Product](
        success=True,
        message="Product updated successfully",
        data=db_product
    )

@router.delete("/{product_id}", response_model=Message)
async def delete_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    """Delete a product"""
    db_product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if not db_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    db.delete(db_product)
    db.commit()
    return Message(message="Product deleted successfully")

@router.get("/{product_id}/prices", response_model=ResponseModel[List[Price]])
async def get_product_prices(
    product_id: int,
    days: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Get price history for a product"""
    # Check if product exists
    if not db.query(ProductModel).filter(ProductModel.id == product_id).first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    query = db.query(PriceModel).filter(PriceModel.product_id == product_id)
    
    if days is not None:
        from datetime import datetime, timedelta
        date_threshold = datetime.utcnow() - timedelta(days=days)
        query = query.filter(PriceModel.created_at >= date_threshold)
    
    prices = query.order_by(PriceModel.created_at.desc()).all()
    return ResponseModel[List[Price]](
        success=True,
        data=prices
    )

@router.get("/{product_id}/latest-price", response_model=ResponseModel[Price])
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
