from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sqlalchemy.orm import Session
from sqlalchemy import func
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from backend.models.database import Product, PriceHistory, ProductAnalytics
import logging

logger = logging.getLogger(__name__)

class MLPreprocessor:
    def __init__(self, session: Session):
        self.session = session
        self.label_encoders = {}
        self.scalers = {}
        self.tfidf = TfidfVectorizer(max_features=100)
    
    def calculate_price_volatility(self, price_history):
        """Calculate price volatility from historical data"""
        if len(price_history) < 2:
            return 0.0
        
        prices = [p.price for p in price_history]
        return np.std(prices) / np.mean(prices) if np.mean(prices) > 0 else 0.0

    def determine_price_range(self, price, category_stats):
        """Determine price range category based on category statistics"""
        mean, std = category_stats['mean'], category_stats['std']
        if price < mean - std:
            return 'budget'
        elif price > mean + std:
            return 'premium'
        return 'mid_range'

    def extract_text_features(self, products):
        """Extract features from product descriptions using TF-IDF"""
        descriptions = [p.description or '' for p in products]
        return self.tfidf.fit_transform(descriptions)

    def get_category_statistics(self):
        """Get price statistics per category"""
        stats = {}
        categories = self.session.query(Product.category).distinct().all()
        
        for (category,) in categories:
            prices = (self.session.query(PriceHistory.price)
                     .join(Product)
                     .filter(Product.category == category)
                     .all())
            prices = [p[0] for p in prices]
            
            if prices:
                stats[category] = {
                    'mean': np.mean(prices),
                    'std': np.std(prices),
                    'min': min(prices),
                    'max': max(prices)
                }
        
        return stats

    def prepare_features(self, lookback_days=30):
        """Prepare features for ML models"""
        logger.info("Starting feature preparation...")
        
        # Get current products with their latest prices
        current_time = datetime.utcnow()
        lookback_date = current_time - timedelta(days=lookback_days)
        
        products = self.session.query(Product).all()
        category_stats = self.get_category_statistics()
        
        for product in products:
            try:
                # Get price history for volatility calculation
                price_history = (self.session.query(PriceHistory)
                               .filter(PriceHistory.product_id == product.id,
                                     PriceHistory.timestamp >= lookback_date)
                               .order_by(PriceHistory.timestamp.desc())
                               .all())
                
                if not price_history:
                    continue
                
                latest_price = price_history[0]
                
                # Calculate analytics
                volatility = self.calculate_price_volatility(price_history)
                price_range = self.determine_price_range(
                    latest_price.price,
                    category_stats.get(product.category, {'mean': 0, 'std': 0})
                )
                
                # Count competitors (products with similar name in same category)
                competitor_count = (self.session.query(func.count(Product.id))
                                 .filter(Product.category == product.category,
                                        Product.id != product.id)
                                 .scalar())
                
                # Calculate average price
                avg_price = np.mean([p.price for p in price_history])
                
                # Update or create analytics record
                analytics = (self.session.query(ProductAnalytics)
                           .filter_by(product_id=product.id)
                           .first() or ProductAnalytics(product_id=product.id))
                
                analytics.avg_price = avg_price
                analytics.price_volatility = volatility
                analytics.price_range = price_range
                analytics.competitor_count = competitor_count
                analytics.market_position = self.determine_market_position(
                    product, category_stats.get(product.category, {})
                )
                analytics.last_updated = current_time
                
                if not analytics.id:  # New record
                    self.session.add(analytics)
                
                logger.info(f"Processed features for product {product.id}")
                
            except Exception as e:
                logger.error(f"Error processing product {product.id}: {str(e)}")
                continue
        
        try:
            self.session.commit()
            logger.info("Successfully updated all product analytics")
        except Exception as e:
            logger.error(f"Error committing analytics updates: {str(e)}")
            self.session.rollback()
            raise

    def determine_market_position(self, product, category_stats):
        """Determine market position based on price, rating, and reviews"""
        if not category_stats or not product.rating:
            return 'unknown'
        
        # Get latest price
        latest_price = (self.session.query(PriceHistory)
                       .filter_by(product_id=product.id)
                       .order_by(PriceHistory.timestamp.desc())
                       .first())
        
        if not latest_price:
            return 'unknown'
        
        # Calculate position based on price and rating
        price_score = (latest_price.price - category_stats.get('mean', 0)) / category_stats.get('std', 1)
        rating_score = product.rating - 3.0  # Center around 3 stars
        
        # Combined score weighted by review count
        review_weight = min(1.0, (product.review_count or 0) / 100)  # Cap at 100 reviews
        combined_score = (price_score + rating_score) * review_weight
        
        if combined_score > 1:
            return 'premium_quality'
        elif combined_score > 0:
            return 'good_value'
        elif combined_score > -1:
            return 'economy'
        else:
            return 'budget'

    def get_training_data(self):
        """Get prepared data for ML training"""
        products = self.session.query(Product).all()
        
        if not products:
            return None, None
        
        # Prepare feature matrix
        features = []
        labels = []
        
        for product in products:
            analytics = product.analytics
            if not analytics or not product.rating:
                continue
                
            feature_vector = [
                analytics.avg_price or 0,
                analytics.price_volatility or 0,
                product.rating or 0,
                product.review_count or 0,
                analytics.competitor_count or 0
            ]
            
            # Add encoded categorical variables
            for field in ['category', 'brand']:
                value = getattr(product, field)
                if value not in self.label_encoders:
                    self.label_encoders[field] = LabelEncoder()
                    self.label_encoders[field].fit([value])
                encoded = self.label_encoders[field].transform([value])[0]
                feature_vector.append(encoded)
            
            features.append(feature_vector)
            
            # Use price_range as label
            labels.append(analytics.price_range)
        
        if not features:
            return None, None
        
        # Convert to numpy arrays
        X = np.array(features)
        y = np.array(labels)
        
        # Scale features
        if 'standard' not in self.scalers:
            self.scalers['standard'] = StandardScaler()
            X = self.scalers['standard'].fit_transform(X)
        else:
            X = self.scalers['standard'].transform(X)
        
        return X, y
