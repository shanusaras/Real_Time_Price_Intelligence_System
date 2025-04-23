"""
ML Model Placeholder
- Load cleaned data
- Train price prediction or discount forecasting model
"""
from sklearn.ensemble import RandomForestRegressor
import pandas as pd
import os

def train_model():
    # Load data
    data_path = os.path.join(os.path.dirname(__file__), '..', 'etl', 'output', 'jumia_products_clean.csv')
    df = pd.read_csv(data_path)
    # TODO: Feature engineering
    X = df[['price']].fillna(0).values  # placeholder features
    y = df['price'].values
    model = RandomForestRegressor()
    model.fit(X, y)
    print("Model trained on price data. Placeholder only.")
    return model

if __name__ == '__main__':
    train_model()
