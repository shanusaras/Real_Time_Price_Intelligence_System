from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from ..database import get_db
from ..models import Category as CategoryModel
from ..schemas.category import Category, CategoryCreate, CategoryUpdate, CategoryInDB
from ..schemas.base import ResponseModel, Message

router = APIRouter(
    prefix="/categories",
    tags=["categories"]
)

@router.get("/", response_model=ResponseModel[List[Category]])
async def get_categories(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    """Get a list of categories with pagination"""
    categories = db.query(CategoryModel).offset(skip).limit(limit).all()
    return ResponseModel[List[Category]](
        success=True,
        data=categories
    )

@router.post("/", response_model=ResponseModel[Category], status_code=status.HTTP_201_CREATED)
async def create_category(
    category: CategoryCreate, 
    db: Session = Depends(get_db)
):
    """Create a new category"""
    db_category = CategoryModel(**category.model_dump())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return ResponseModel[Category](
        success=True,
        message="Category created successfully",
        data=db_category
    )

@router.get("/{category_id}", response_model=ResponseModel[Category])
async def get_category(
    category_id: int, 
    db: Session = Depends(get_db)
):
    """Get a single category by ID"""
    db_category = db.query(CategoryModel).filter(CategoryModel.id == category_id).first()
    if db_category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    return ResponseModel[Category](
        success=True,
        data=db_category
    )

@router.put("/{category_id}", response_model=ResponseModel[Category])
async def update_category(
    category_id: int,
    category: CategoryUpdate,
    db: Session = Depends(get_db)
):
    """Update a category"""
    db_category = db.query(CategoryModel).filter(CategoryModel.id == category_id).first()
    if db_category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    
    update_data = category.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_category, field, value)
    
    db.commit()
    db.refresh(db_category)
    return ResponseModel[Category](
        success=True,
        message="Category updated successfully",
        data=db_category
    )

@router.delete("/{category_id}", response_model=Message)
async def delete_category(
    category_id: int,
    db: Session = Depends(get_db)
):
    """Delete a category"""
    db_category = db.query(CategoryModel).filter(CategoryModel.id == category_id).first()
    if db_category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    
    db.delete(db_category)
    db.commit()
    return Message(message="Category deleted successfully")
