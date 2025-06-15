import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from api.main import app
from api.database import Base, get_db

# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create test database
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# Override the database dependency
app.dependency_overrides[get_db] = override_get_db

# Test client
client = TestClient(app)

def setup_module(module):
    # Create the database tables
    Base.metadata.create_all(bind=engine)
    # Add test data
    db = TestingSessionLocal()
    try:
        # Add test categories
        from api.models import Category, Product, Price
        from datetime import datetime, timedelta
        
        # Add test category
        category = Category(name="Test Category")
        db.add(category)
        db.commit()
        
        # Add test product
        product = Product(
            name="Test Product",
            brand="Test Brand",
            category_id=category.id,
            link="http://example.com/product/1"
        )
        db.add(product)
        db.commit()
        
        # Add price history
        for i in range(10):
            price = Price(
                product_id=product.id,
                price=100.0 - i * 5.0,
                discount_pct=i * 5,
                in_stock=True,
                timestamp=datetime.utcnow() - timedelta(days=9-i)
            )
            db.add(price)
        db.commit()
        
    finally:
        db.close()

def teardown_module(module):
    # Clean up the database
    Base.metadata.drop_all(bind=engine)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_list_products():
    response = client.get("/api/v1/products/")
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert isinstance(data["data"], list)
    assert data["total"] > 0

def test_get_product():
    response = client.get("/api/v1/products/1")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Product"
    assert data["brand"] == "Test Brand"

def test_get_product_not_found():
    response = client.get("/api/v1/products/999")
    assert response.status_code == 404

def test_get_price_history():
    response = client.get("/api/v1/products/1/prices")
    assert response.status_code == 200
    data = response.json()
    assert data["product_id"] == 1
    assert len(data["prices"]) > 0

def test_analytics_price_stats():
    response = client.get("/api/v1/analytics/price-stats")
    assert response.status_code == 200
    data = response.json()
    assert "price_stats" in data
    assert "average" in data["price_stats"]

def test_analytics_category_stats():
    response = client.get("/api/v1/analytics/category-stats")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if len(data) > 0:
        assert "category_name" in data[0]
