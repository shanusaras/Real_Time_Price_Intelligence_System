import streamlit as st
import pandas as pd
import plotly.express as px
from backend.models.db_manager import DatabaseManager
from ml_preprocessor import MLPreprocessor
from price_predictor import PricePredictor
import numpy as np
from datetime import datetime, timedelta

# Page config
st.set_page_config(
    page_title="Price Intelligence Dashboard",
    page_icon="📊",
    layout="wide"
)

# Initialize database and ML components
db = DatabaseManager()
session = db.get_session()
preprocessor = MLPreprocessor(session)
predictor = PricePredictor()

# Sidebar filters
st.sidebar.title("Filters")
days = st.sidebar.slider("Days of History", 7, 90, 30)
min_price = st.sidebar.number_input("Min Price", 0)
max_price = st.sidebar.number_input("Max Price", 0)

# Main content
st.title("Price Intelligence Dashboard")

# Get data
with session:
    # Get recent price changes
    price_changes = pd.read_sql(
        f"""
        SELECT 
            p.name,
            ph.price,
            ph.original_price,
            ph.discount_percentage,
            ph.timestamp
        FROM products p
        JOIN price_history ph ON p.id = ph.product_id
        WHERE ph.timestamp >= DATE_SUB(NOW(), INTERVAL {days} DAY)
        """,
        session.bind
    )

# Price Trends
st.header("Price Trends")
col1, col2 = st.columns(2)

with col1:
    # Price over time
    fig_price = px.line(
        price_changes,
        x="timestamp",
        y="price",
        title="Price Trends Over Time"
    )
    st.plotly_chart(fig_price)

with col2:
    # Discount distribution
    fig_discount = px.histogram(
        price_changes,
        x="discount_percentage",
        title="Discount Distribution"
    )
    st.plotly_chart(fig_discount)

# Price Range Analysis
st.header("Price Range Analysis")
col3, col4 = st.columns(2)

with col3:
    # Price distribution
    fig_price_dist = px.histogram(
        price_changes,
        x="price",
        title="Price Distribution"
    )
    st.plotly_chart(fig_price_dist)

with col4:
    # Price vs Original Price scatter
    fig_scatter = px.scatter(
        price_changes,
        x="original_price",
        y="price",
        title="Price vs Original Price"
    )
    st.plotly_chart(fig_scatter)

# ML Insights
st.header("ML Insights")

if st.button("Update ML Models"):
    with st.spinner("Training models..."):
        X, y = preprocessor.get_training_data()
        if X is not None and y is not None:
            success = predictor.train_models(X, y)
            if success:
                st.success("Models trained successfully!")
            else:
                st.error("Error training models")
        else:
            st.warning("No training data available")

# Feature Importance
importance = predictor.get_feature_importance()
if importance:
    col5, col6 = st.columns(2)
    
    with col5:
        # Price Range Feature Importance
        range_imp = pd.DataFrame({
            'feature': range(len(importance['price_range']['importance'])),
            'importance': importance['price_range']['importance']
        }).sort_values('importance', ascending=False)
        
        fig_range_imp = px.bar(
            range_imp,
            x='feature',
            y='importance',
            title='Price Range Feature Importance'
        )
        st.plotly_chart(fig_range_imp)
    
    with col6:
        # Price Prediction Feature Importance
        price_imp = pd.DataFrame({
            'feature': range(len(importance['price']['importance'])),
            'importance': importance['price']['importance']
        }).sort_values('importance', ascending=False)
        
        fig_price_imp = px.bar(
            price_imp,
            x='feature',
            y='importance',
            title='Price Prediction Feature Importance'
        )
        st.plotly_chart(fig_price_imp)

# Recent Predictions
st.header("Recent Predictions")
recent_data = preprocessor.prepare_recent_data()
if recent_data is not None:
    predictions = pd.DataFrame({
        'Product': recent_data['names'],
        'Actual Price': recent_data['prices'],
        'Predicted Price': predictor.predict_price(recent_data['features']),
        'Price Range': predictor.predict_price_range(recent_data['features'])
    })
    st.dataframe(predictions)
