# Price Intelligence API

A FastAPI-based RESTful API for tracking and analyzing product prices across different e-commerce platforms.

## Features

- Product management (CRUD operations)
- Category management
- Price history tracking
- RESTful endpoints with proper status codes
- Input validation using Pydantic
- SQLAlchemy ORM integration
- Automatic API documentation with Swagger UI and ReDoc

## Prerequisites

- Python 3.8+
- pip (Python package manager)
- SQLite (for development, included with Python)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd price-intelligence-system
   ```

2. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

Create a `.env` file in the project root with the following variables:

```env
DATABASE_URL=sqlite:///./price_intelligence.db
API_V1_STR=/api/v1
PROJECT_NAME=Price Intelligence API
CORS_ORIGINS=["*"]
```

## Database Setup

The API uses SQLite by default for development. The database will be automatically created when you first run the application.

## Running the Application

Start the development server:

```bash
uvicorn api.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`

## API Documentation

- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

## API Endpoints

### Base
- `GET /` - API welcome message
- `GET /health` - Health check
- `GET /info` - API information

### Categories
- `GET /categories/` - List all categories
- `POST /categories/` - Create a category
- `GET /categories/{id}` - Get a category
- `PUT /categories/{id}` - Update a category
- `DELETE /categories/{id}` - Delete a category

### Products
- `GET /products/` - List all products
- `POST /products/` - Create a product
- `GET /products/{id}` - Get a product
- `PUT /products/{id}` - Update a product
- `DELETE /products/{id}` - Delete a product
- `GET /products/{id}/prices` - Get price history for a product

### Prices
- `POST /prices/` - Add a price entry
- `GET /prices/{id}` - Get a price entry
- `GET /prices/product/{product_id}/latest` - Get latest price for a product
- `GET /prices/product/{product_id}/history` - Get price history for a product

## Development

### Running Tests

```bash
pytest
```

### Code Style

This project uses:
- Black for code formatting
- Flake8 for linting
- isort for import sorting

Run the following commands before committing:

```bash
black .
isort .
flake8
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
