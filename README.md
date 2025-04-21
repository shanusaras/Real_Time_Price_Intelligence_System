# 🛒 Real-Time Price Intelligence System

A scalable, end-to-end simulation of a real-world **Price Intelligence System** for e-commerce, powered by clean pipelines, structured data, and business-aligned insights.

---

## 🚧 Project Status: Phase 1 Complete

**✔ 20,000+ products scraped**  
**✔ Robust data pipeline built**  
**✔ Business-driven categorization logic applied**  
➡️ *Next: EDA, ML modeling, real-time dashboard, deployment*

---

## 📦 Project Summary

In e-commerce, pricing strategy is critical — it directly affects revenue, profit margins, and market competitiveness. This project builds the foundation of a system that helps businesses:

- Continuously **track competitor pricing**
- **Analyze price trends**
- Optimize pricing using **ML-based recommendations**

---

## 🔁 Phase 1: Scalable Data Collection Pipeline

To simulate real-world scale:

- ✅ Scraped **20,000+ products** using the [Open Food Facts API](https://world.openfoodfacts.org/data)
- ✅ Covered **15 major categories × 120+ pages**
- ✅ Generated structured data in **JSON + CSV** formats

### ⚙️ Pipeline Features:

- Retry logic with **exponential backoff**
- Rate-limiting to avoid IP bans
- Logging + fault tolerance
- **Post-scraping categorization** using business keywords:
  - Snacks
  - Beverages
  - Dairy
  - Personal Care
  - Health Supplements

### 🧠 Why Open Food Facts?

Attempted Flipkart scraping but faced heavy anti-bot protection. Pivoted to Open Food Facts — an open-source, ethical, large-scale API ideal for simulation.

---

## 📁 Project Structure

Real_Time_Price_Intelligence_System/ │ ├── data/ → Raw + cleaned datasets (JSON, CSV) ├── notebooks/ → Jupyter Notebooks (EDA, Modeling) ├── scripts/ → Data scraping, transformation scripts ├── dashboards/ → Streamlit (planned) ├── models/ → Trained ML models (upcoming) ├── requirements.txt → Python dependencies └── README.md → You are here

---

## 🛠️ Tech Stack

- **Python** (Requests, Pandas, NumPy, JSON, Regex)
- **API Handling** (Open Food Facts)
- **Data Processing** (Pandas)
- **Visualization** (Matplotlib, Seaborn – upcoming)
- **ML Modeling** (scikit-learn – upcoming)
- **Dashboards** (Streamlit – upcoming)

---

## 📊 What’s Next

- 📌 Exploratory Data Analysis (EDA) on pricing patterns
- 📌 Real-time interactive dashboard with filters
- 📌 ML model to detect price anomalies + suggest optimal pricing
- 📌 Full **ETL → ML → Deployment** pipeline

---

## 💡 Key Learnings

- Reliable scraping pipelines must be **fault-tolerant, ethical, and scalable**
- **Business-aligned categorization** beats raw category tags
- Clean, structured data unlocks downstream insights and automation

---

## 🤝 Connect & Discuss

Curious what pricing signals **you** think are most critical for modern e-commerce?  
Drop a suggestion or open an issue!

📬 [LinkedIn](https://www.linkedin.com/in/shanusaraswat) | [Project Post](#) *(add your live post URL)*

---

## 📄 License

MIT License — feel free to fork, build on, or improve.

---

## 🙌 Contributions

Got an idea or improvement? PRs and suggestions are welcome.
