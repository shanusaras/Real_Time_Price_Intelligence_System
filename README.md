# 🛒 Real-Time Price Intelligence System

A scalable, end-to-end simulation of a real-world **Price Intelligence System** for e-commerce, powered by clean pipelines, structured data, and business-aligned insights.

---

## 🚧 Project Status: Phase 1 Complete

- **✔ Scalable Jumia data scraping implemented**  
- **✔ Robust data pipeline built**  
- **✔ Business-driven categorization logic applied**  
- ➡️ *Next: ETL & data cleaning, API endpoints, ML modeling, dashboard visualization*

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
├── data_collection/               # Scraper and raw data
│   ├── data/                      # Raw JSON outputs
│   │   ├── jumia_playwright.json
│   │   └── sample_by_category.json
│   └── scrape_jumia_playwright.py # Playwright-based Jumia scraper
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

## 🛠️ Tech Stack

- **Python** (Playwright, Pandas, NumPy)  
- **API** (FastAPI)  
- **Data Processing** (Pandas)  
- **Visualization** (Streamlit – upcoming)  
- **ML Modeling** (scikit-learn – upcoming)  
- **Containerization** (Docker)

---

## Next Steps
- Scaffold `etl/` directory and add loader script
- Define table schemas and transformation logic
- Schedule ETL jobs (e.g., Airflow)
- Exploratory Data Analysis (EDA) on pricing patterns
- Real-time interactive dashboard with filters
- ML model to detect price anomalies + suggest optimal pricing
- Full **ETL → ML → Deployment** pipeline

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
