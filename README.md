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

## Project Phases & Roadmap

### Phase 1: Data Collection
Folder: `data_collection/`
- Scripts to scrape OpenFoodFacts and Flipkart
- Implement proxy rotation, rate limiting, retries
- Save raw JSON outputs in `data_collection/data/`

### Phase 2: Data Storage & ETL
Folder: `etl/`
- `load_to_mysql.py`: Bulk load full JSON from `data_collection/data/` into MySQL
- `transform.py`: Clean, normalize, enrich data (pandas or SQL)
- `sql/`: DDL for tables, views, stored procedures
- `config/`: Connection templates, env parsing

### Phase 3: API & Backend Services
Folder: `api/`
- FastAPI endpoints for querying products, categories
- Swagger/OpenAPI docs
- Dockerfile for API service

### Phase 4: Dashboard & Visualization
Folder: `dashboard/`
- Streamlit or React dashboard for trends and comparisons
- Charts: price over time, category comparisons
- Dockerfile for dashboard service

### Phase 5: Advanced Analytics & ML
Folder: `ml/`
- Price forecasting models (time series)
- Anomaly detection on price changes
- Market basket analysis
- Automated insights via scheduled jobs

### Phase 6: Integration & Deployment
- Container orchestration (Docker Compose / Kubernetes)
- CI/CD pipelines (GitHub Actions)
- Monitoring & alerts

## Project Structure
```plaintext
Real_Time_Price_Intelligence_System/
├── data_collection/               # Scraping scripts and utilities
│   ├── data/                      # Raw JSON outputs
│   ├── create_sample_from_dataset.py
│   ├── extract_categories_from_all_products.py
│   ├── fetch_top_categories_products.py
│   ├── scrape_all_products.py
│   ├── scrape_top_categories_direct.py
│   └── [*.log]                    # Log files
├── docker-compose.yml             # Services definitions
├── .env.template                  # Environment variables template
├── requirements.txt               # Python dependencies
├── .pre-commit-config.yaml        # Security hooks config
├── .gitignore                     # Ignored files
├── README.md                      # Project documentation
├── git-filter-repo/               # Git filter repository data
└── venv/                          # Virtual environment (ignored)
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
- Scaffold `etl/` directory and add loader script
- Define table schemas and transformation logic
- Schedule ETL jobs (e.g., Airflow)

## License
MIT License – see [LICENSE](LICENSE) for details.