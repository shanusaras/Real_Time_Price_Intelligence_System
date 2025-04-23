from fastapi import FastAPI
import pandas as pd
import os

app = FastAPI(title="Price Intelligence API")

# Load cleaned data if exists
data_path = os.path.join(os.path.dirname(__file__), '..', 'etl', 'output', 'jumia_products_clean.csv')

@app.get('/')
def root():
    return {"message": "API running"}

@app.get('/products')
def get_products(limit: int = 100):
    """Return a subset of products"""
    if os.path.exists(data_path):
        df = pd.read_csv(data_path)
        records = df.head(limit).to_dict(orient='records')
        return records
    return []
