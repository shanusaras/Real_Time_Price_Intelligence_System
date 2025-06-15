"""
Database session management for SQLAlchemy.

This module provides session factories and utilities for database access.
"""
from typing import AsyncGenerator, Generator

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import NullPool

from ..config import settings

# Synchronous engine for migrations and sync operations
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,  # Recycle connections after 5 minutes
    echo=settings.DEBUG,
)

# Asynchronous engine for async operations
async_engine = create_async_engine(
    settings.ASYNC_DATABASE_URL or settings.DATABASE_URL.replace('sqlite://', 'sqlite+aiosqlite://'),
    echo=settings.DEBUG,
    pool_pre_ping=True,
    pool_recycle=300,
    poolclass=NullPool if settings.TESTING else None,
    future=True
)

# Session factories
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False
)

AsyncSessionLocal = sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    future=True
)

def get_db() -> Generator[Session, None, None]:
    """
    Dependency for getting a synchronous database session.
    
    Yields:
        Session: A SQLAlchemy database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency for getting an asynchronous database session.
    
    Yields:
        AsyncSession: An async SQLAlchemy database session
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
