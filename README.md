# Real-Time Price Intelligence System

## Overview
A demonstration project that builds a scalable pipeline for real-time price analytics. It covers data collection, storage, API service, and interactive dashboards, all orchestrated via Docker.

## Current Focus
**Phase 1 – Data Collection**: Enhancing multi-category scraping with proxy rotation, rate limiting, and robust error handling for continuous data ingestion.

## Features Completed
- **Data Collection**: Python scripts to fetch multi-category data from Open Food Facts API with retries, logging, and pagination.
- **Storage & ETL**: MySQL integration via Docker Compose; automated ETL to transform raw JSON into structured tables.
- **API Service**: FastAPI backend exposing REST endpoints for price retrieval and analytics.
- **Dashboard**: Streamlit app for visualizing price trends and category comparisons.
- **Infrastructure & Security**: Docker Compose orchestration; environment variables for credentials; pre-commit hooks for secrets and large-file detection; comprehensive `.gitignore`.

## Tech Stack
- **Language**: Python 3.8+
- **API**: FastAPI
- **Database**: MySQL 8.0
- **Dashboard**: Streamlit
- **Containerization**: Docker & Docker Compose
- **CI**: pre-commit hooks (detect-aws-credentials, detect-private-key, large-file checks, secret_scanner)

## Project Structure
```plaintext
Real_Time_Price_Intelligence_System/
├── data_collection/         # Scraping scripts
│   ├── fetch_openfoodfacts_products.py
│   ├── extract_categories_from_all_products.py
│   └── create_sample_from_dataset.py
├── data/                    # Raw JSON outputs
├── api/                     # FastAPI service and Dockerfile
│   └── api.Dockerfile
├── dashboard/               # Streamlit app and Dockerfile
│   └── dashboard.Dockerfile
├── docker-compose.yml       # Services definitions (with env placeholders)
├── .pre-commit-config.yaml  # Security hooks config
├── .gitignore               # Ignored files
└── README.md                # Project documentation
```

## Getting Started
### Prerequisites
- Docker & Docker Compose
- Python 3.8+ (for local scripts)

### Installation
```bash
# Clone the repository
git clone https://github.com/shanusaras/Real_Time_Price_Intelligence_System.git
cd Real_Time_Price_Intelligence_System
# Prepare environment variables
cp .env.example .env
# Edit .env with your MySQL credentials
```

### Launch Services
```bash
docker-compose up --build
```

## Usage
- **Run Data Collection:** `python data_collection/fetch_openfoodfacts_products.py`
- **API Documentation:** http://localhost:8000/docs
- **Dashboard:** http://localhost:8501

## Environment Variables
Add these to your `.env` file:
```ini
MYSQL_ROOT_PASSWORD=your_root_password
MYSQL_DATABASE=price_intelligence
MYSQL_HOST=mysql
MYSQL_USER=root
MYSQL_PASSWORD=your_db_password
```

## Next Steps
- Implement proxy rotation and continuous scraping enhancements.
- Develop advanced analytics and ML models.
- Add automated alerts and reporting.
- Integrate CI/CD security and testing workflows.

## License
MIT License – see [LICENSE](LICENSE) for details.