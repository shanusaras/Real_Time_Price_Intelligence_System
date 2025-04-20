# Real Time Price Intelligence System

## 🎯 Project Overview
An educational demonstration project showcasing a modern data pipeline for price analytics. This system demonstrates various aspects of data engineering, machine learning, and full-stack development.

## ⚠️ Important Disclaimers

### Educational Purpose
- This project is created for **educational and demonstration purposes only**
- It serves as a portfolio piece to showcase technical implementation skills
- Not intended for production use or commercial deployment

### Ethical Considerations
- Implements responsible data collection practices
- Respects website terms of service and robots.txt
- Uses rate limiting and caching to minimize server load
- Does not collect personal or private information
- Data is used solely for educational purposes

## 🏗️ System Architecture

## 📥 Data Collection Process

### Overview
- **Source:** Open Food Facts API (global, open dataset with millions of food/grocery products)
- **Goal:** Collect a large, multi-category dataset (25,000+ products) for analytics and demonstration
- **Approach:** Robust, scalable Python script with rate limiting, error handling, and progress logging

### Design Decisions
- **API-based collection:** Chosen for reliability, legality, and scalability
- **Multi-category support:** Open Food Facts provides products from a wide range of categories (dairy, beverages, snacks, etc.)
- **Rate limiting:** Script pauses between API requests to respect server load and demonstrate best practices
- **Error handling:** Implements retries, logs errors, and skips problematic pages for uninterrupted collection
- **Scalability:** Designed to handle tens of thousands of records efficiently

### How It Works
- Fetches products in batches (pages) using the Open Food Facts API
- Retries failed requests up to 3 times with exponential backoff
- Logs errors to `scrape_all_products_errors.log` for transparency
- Saves the complete dataset to `all_products_openfoodfacts.json` for downstream ETL and analytics

### Data Collection Folder Structure & Workflow

The `data_collection/` folder is organized for maximum clarity and ease of use:

| File/Folder                           | Purpose                                                      |
|---------------------------------------|--------------------------------------------------------------|
| scrape_all_products.py                | Main, broad scraper for all products (up to 25,000)          |
| extract_categories_from_all_products.py| Categorizes the all-products dataset into 5 business-relevant categories |
| create_sample_from_dataset.py         | Creates a 100-record sample from any dataset for demo/testing |
| scrape_top_categories_direct.py       | (Optional) Directly scrapes only the top 5 business categories from the API |
| scrape_all_products.log               | Log file for main scraping script                            |
| scrape_all_products_errors.log        | Error log for main scraper                                   |
| scrape_top_categories_direct.log      | Log file for direct multi-category scraping                  |
| data/                                | All JSON data files (outputs from scripts)                   |
| ├── all_products_openfoodfacts.json   | Full general dataset (25,000 products)                       |
| ├── sample_all_products.json          | 100-record sample for demo/testing                           |
| ├── all_products_by_category.json     | Products grouped by the 5 business categories                |
| └── top_categories_direct_scrape.json | (Optional) Direct scrape of top 5 categories                 |

#### Recommended Workflow

1. **Broad Scraping:**
   - Run `scrape_all_products.py` to collect all products (`all_products_openfoodfacts.json`).
   - Logs: `scrape_all_products.log`, errors in `scrape_all_products_errors.log`.
2. **Category Extraction:**
   - Run `extract_categories_from_all_products.py` to group products by business category (`all_products_by_category.json`).
   - **For this project, all further analysis and dashboards use `all_products_by_category.json` as the primary input.**
   - **Rationale:** Using a categorized file mirrors real-world business analytics, where segmentation by category enables more actionable insights, targeted visualizations, and practical decision-making. This approach ensures the pipeline reflects real-world problem-solving and business intelligence best practices.
3. **Sample Creation:**
   - Run `create_sample_from_dataset.py` to create a small sample (`sample_all_products.json`).
4. **(Optional) Direct Category Scraping:**
   - Run `scrape_top_categories_direct.py` to scrape only the 5 business categories (`top_categories_direct_scrape.json`).
   - Log: `scrape_top_categories_direct.log`.

This structure makes it easy to identify, run, and analyze each stage of the data pipeline for both demonstration and practical use.

### Sample Output

<details>
<summary>Click to view sample product data</summary>

```json
[
  {
    "product_name": "Coca-Cola",
    "brands": "Coca-Cola",
    "categories": "Beverages, Carbonated drinks, Sodas",
    "countries": "United States, France, Germany",
    "quantity": "330 ml",
    "stores": "Walmart, Carrefour",
    "nutriments": {
      "energy_100g": 180,
      "sugars_100g": 10.6,
      "fat_100g": 0
      // ... more fields
    }
    // ... more fields
  },
  ...
]
```
</details>

### Reproducibility
- **Script:** `data_collection/fetch_openfoodfacts_products.py`
- **How to run:**
  ```bash
  python data_collection/fetch_openfoodfacts_products.py
  ```
- **Output location:** `data_collection/data/openfoodfacts_products.json`


### 1. Data Collection
- Ethical web data collection with rate limiting
- Response caching to minimize requests
- Multi-category support
- Price range filtering

### 2. Data Storage & ETL
- MySQL database for structured data storage
- ETL pipeline for data transformation
- Historical price tracking

### 3. Machine Learning Pipeline
- Price trend analysis
- Automated feature engineering
- Model training pipeline

### 4. API & Backend Services
- FastAPI backend
- RESTful API endpoints
- Authentication and rate limiting

### 5. Dashboard & Visualization
- Streamlit-based dashboard
- Interactive price analytics
- Trend visualization

### 6. Infrastructure
- Docker containerization
- Service orchestration
- Monitoring and logging

## 🛠️ Tech Stack
- **Backend**: Python, FastAPI
- **Database**: MySQL
- **ML/Analytics**: Pandas, Scikit-learn
- **Frontend**: Streamlit
- **Infrastructure**: Docker

## 🚀 Getting Started

### Prerequisites
```bash
pip install -r requirements.txt
```

### Running the System
```bash
docker-compose up
```

## 📊 Features
- Multi-category price tracking
- Historical price analysis
- Price trend visualization
- Automated price alerts
- RESTful API access

## 🔒 Security & Ethics
- Implements rate limiting
- Respects robots.txt
- Proper user-agent identification
- Response caching
- No personal data collection

## 🤝 Contributing
This is an educational project. While contributions are welcome, please ensure they align with the project's educational goals and ethical guidelines.

## 📝 License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments
- Built for educational purposes
- Demonstrates modern software architecture
- Showcases ethical data practices

A full-stack analytics solution for e-commerce price intelligence and market analysis.

## Features

- Real-time price tracking and analysis
- Historical price trend visualization
- Competitor price analysis
- Demand forecasting
- Interactive analytics dashboard

## Tech Stack

### Backend
- FastAPI (REST API)
- PostgreSQL (Structured Data)
- MongoDB (Semi-structured Data)
- Apache Airflow (Data Pipeline)
- Prophet (Time Series Forecasting)

### Frontend
- React
- Plotly (Data Visualization)
- Material-UI

## Project Structure

```
├── backend/
│   ├── api/           # FastAPI application
│   ├── data_pipeline/ # Airflow DAGs and ETL scripts
│   └── models/        # Database models and schemas
├── frontend/
│   └── src/
│       ├── components/
│       └── pages/
├── config/           # Configuration files
├── data/
│   ├── raw/         # Raw data files
│   └── processed/    # Processed data files
└── requirements.txt
```

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy `.env.example` to `.env` and fill in your configuration
5. Initialize the database:
   ```bash
   python backend/models/database.py
   ```
6. Start the API server:
   ```bash
   uvicorn backend.api.main:app --reload
   ```

## Data Pipeline

The data pipeline uses Apache Airflow to:
1. Extract data from various sources
2. Transform and clean the data
3. Load processed data into the database
4. Generate analytics and insights

## Analytics Features

- Price trend analysis
- Seasonal patterns detection
- Competitor price comparison
- Demand forecasting
- Market positioning analysis

## API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT