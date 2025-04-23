import streamlit as st
import pandas as pd
import os

st.title("Real-Time Jumia Price Dashboard")

# Load cleaned data
data_path = os.path.join(os.path.dirname(__file__), '..', 'etl', 'output', 'jumia_products_clean.csv')
if os.path.exists(data_path):
    df = pd.read_csv(data_path)
    st.write(f"Loaded {len(df)} products")
    st.dataframe(df.head(10))
else:
    st.warning("No data found. Please run ETL transform first.")
