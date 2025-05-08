# 🛒 Real-Time Price Intelligence System

A scalable, end-to-end simulation of a real-world **Price Intelligence System** for e-commerce, powered by clean pipelines, structured data, and business-aligned insights.

---

## 🚦 Project Status: API & Analytics Ready

- **✔ Scalable Jumia data scraping implemented**  
- **✔ Robust ETL pipeline built (JSON → MySQL)**  
- **✔ Data cleaning, deduplication, normalization complete**  
- **✔ Core API endpoints for product analytics, category insights, and KPIs implemented & tested**
- ➡️ *Next: ML modeling, dashboard visualization, deployment*

---

## 🛠️ Available API Endpoints

### `/products`
- **Description:** List products with filters (category, brand, price).
- **Business Value:** Enables product search, catalog exploration, and inventory analysis.
- **Example:**
  ```bash
  curl "http://localhost:8000/products?category=phones-accessories&min_price=1000&limit=5"
  ```

### `/price-history`
- **Description:** Get price, rating, and review history for a product.
- **Business Value:** Supports price trend analysis and pricing strategy decisions.
- **Example:**
  ```bash
  curl "http://localhost:8000/price-history?product_id=40490"
  ```

### `/categories`
- **Description:** List categories with product count and price stats.
- **Business Value:** Helps identify popular categories and pricing opportunities.
- **Example:**
  ```bash
  curl "http://localhost:8000/categories"
  ```

### `/top-rated`
- **Description:** Top-rated products (latest data, deduplicated).
- **Business Value:** Identify trending and high-quality products for promotion or analysis.
- **Example:**
  ```bash
  curl "http://localhost:8000/top-rated?limit=5"
  ```

### `/most-reviewed`
- **Description:** Most-reviewed products (latest data, deduplicated).
- **Business Value:** Surface popular and widely-discussed products for marketing or insights.
- **Example:**
  ```bash
  curl "http://localhost:8000/most-reviewed?limit=5"
  ```

### `/analytics/summary`
- **Description:** Key KPIs: product count, category count, avg price/rating, total reviews.
- **Business Value:** Provides at-a-glance business health metrics for the product catalog.
- **Example:**
  ```bash
  curl "http://localhost:8000/analytics/summary"
  ```

All endpoints use the latest, deduplicated data for accuracy.

---

## 🚧 Next Steps

- Implement ML features (price prediction, anomaly detection)
- Build interactive dashboard (Streamlit)
- Dockerize and deploy full stack

---

## 📦 Project Summary

In e-commerce, pricing strategy is critical — it directly affects revenue, profit margins, and market competitiveness. This project builds the foundation of a system that helps businesses:
- Continuously **track competitor product prices** on Jumia
- **Capture detailed product metadata** (title, brand, price, discount, rating, reviews, availability)
- Optimize pricing and promotional strategies using **data-driven insights**

---

## 🔁 Phase 1: Scalable Data Collection Pipeline

To collect rich pricing data at scale:
- ✅ Scraped **18,983 products** (≈19,000) using Playwright from Jumia
- ✅ Covered **10 major categories × up to 50 pages** per category
- ✅ Stored results in structured **JSON** format (`data_collection/data/jumia_playwright.json`)

### ⚙️ Pipeline Features:
- Retry logic with **exponential backoff**
- Navigation timeouts and **selector-based waits**
- Tracking and skipping of timed-out pages
- Extraction of **brand**, **discount_pct**, **rating**, **reviews**, **in_stock** fields

---

## ⚖️ Ethical Scraping & Disclaimer

We follow these ethical guidelines for all scraping activities:
- Respect **robots.txt** and each site's **Terms of Service**
- Apply **rate limiting** and **proxy rotation** to avoid overloading servers
- Identify our scraper responsibly with a **custom User-Agent**
- Avoid collecting **personal or sensitive data**
- Comply with all applicable **legal regulations and privacy policies**

---

## 📁 Project Structure

```plaintext
Real_Time_Price_Intelligence_System/
├── data_collection/               # Scraper and raw/test data
│   ├── data/                      # Main dataset (for ETL)
│   │   └── jumia_playwright.json
│   └── test_data/                 # Small sample/test data
│       └── sample_by_category.json
│   └── scrape_jumia_playwright.py # Playwright-based Jumia scraper
├── etl/                           # ETL and data cleaning scripts
│   ├── transform.py               # ETL: JSON → MySQL
│   └── models.py                  # SQLAlchemy models
├── api/                           # FastAPI backend
│   └── main.py
├── etl/                           # ETL and data cleaning scripts
│   ├── transform.py
│   └── load_to_mysql.py
├── ml/                            # Machine learning models
│   └── model.py
├── dashboard/                     # Visualization dashboard
│   └── app.py
├── assets/                        # Static assets (images, icons)
├── docker-compose.yml            # Service orchestration
├── requirements.txt              # Python dependencies
├── .env.template                 # Environment variables template
├── .pre-commit-config.yaml       # Linting and security hooks
├── .gitignore                    # Ignored files
└── README.md                     # Project documentation
```

---

## 🧩 ETL Phase: JSON → MySQL

**ETL pipeline loads all scraped product data into a MySQL database for analytics and downstream use.**

### How it works
- Reads Jumia product data from `data_collection/data/jumia_playwright.json`
- Cleans, deduplicates, and normalizes product records
- Loads products and price history into MySQL using SQLAlchemy models (`etl/models.py`)
- Handles special characters, long text fields, and missing values robustly

### How to run
1. Ensure MySQL is running and database `price_intelligence_v2` is created
2. Update `etl/config.py` with your MySQL credentials
3. Create tables (if not already done):
   ```bash
   python etl/create_db_tables.py
   ```
4. Run ETL pipeline:
   ```bash
   python etl/transform.py
   ```
5. Data will be loaded into `products` and `price_history` tables

---

## 🛠️ Tech Stack

- **Python** (Playwright, Pandas, SQLAlchemy, PyMySQL)
- **Database** (MySQL)
- **API** (FastAPI – upcoming)
- **Visualization** (Streamlit – upcoming)
- **ML Modeling** (scikit-learn – upcoming)
- **Containerization** (Docker)

---

## Next Steps
- Build API endpoints (FastAPI) for product & price queries
- Exploratory Data Analysis (EDA) and price analytics
- Real-time interactive dashboard with filters (Streamlit)
- ML model to detect price anomalies + suggest optimal pricing
- Full **ETL → API → ML → Dashboard → Deployment** pipeline

---

## 💡 Key Learnings

- Reliable scraping pipelines must be **fault-tolerant, ethical, and scalable**
- **Business-aligned categorization** beats raw category tags
- Clean, structured data unlocks downstream insights and automation

---

## 🤝 Connect & Discuss

Curious what pricing signals **you** think are most critical for modern e-commerce?  
Drop a suggestion or open an issue!

📬 [LinkedIn](https://www.linkedin.com/in/saraswathi-rajendran-29b962205/) | [Project Post](https://www.linkedin.com/posts/saraswathi-rajendran-29b962205_code-output-data-structure-overview-activity-7320722521702416384-owjx?utm_source=share&utm_medium=member_desktop&rcm=ACoAADRJ8RcBz7fP5ZlIlPiAzGhQ2unlizFiXNQ)

---

## 📄 License

MIT License — feel free to fork, build on, or improve.

---

## 🙌 Contributions

Got an idea or improvement? PRs and suggestions are welcome.
