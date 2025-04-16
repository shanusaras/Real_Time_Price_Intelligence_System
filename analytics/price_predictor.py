from sklearn.ensemble import RandomForestRegressor, GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, classification_report
import numpy as np
import joblib
import logging
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

class PricePredictor:
    def __init__(self, model_dir='models'):
        self.model_dir = Path(model_dir)
        self.model_dir.mkdir(exist_ok=True)
        
        # Initialize models
        self.price_regressor = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        
        self.range_classifier = GradientBoostingClassifier(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=5,
            random_state=42
        )
        
        self.is_trained = False
    
    def train_models(self, X, y, test_size=0.2):
        """Train both regression and classification models"""
        if X is None or y is None:
            logger.error("No training data provided")
            return False
            
        try:
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=test_size, random_state=42
            )
            
            # Train price range classifier
            self.range_classifier.fit(X_train, y_train)
            y_pred_class = self.range_classifier.predict(X_test)
            
            # Log classification results
            logger.info("Price Range Classification Report:")
            logger.info("\n" + classification_report(y_test, y_pred_class))
            
            # Train price regressor on numeric prices
            numeric_prices = np.array([float(p.split('_')[0]) 
                                     if isinstance(p, str) and '_' in p 
                                     else 0.0 for p in y])
            self.price_regressor.fit(X_train, numeric_prices[:-len(X_test)])
            
            # Calculate regression metrics
            y_pred_reg = self.price_regressor.predict(X_test)
            mae = mean_absolute_error(numeric_prices[-len(X_test):], y_pred_reg)
            logger.info(f"Price Prediction MAE: {mae:.2f}")
            
            self.is_trained = True
            
            # Save models
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            joblib.dump(self.range_classifier, 
                       self.model_dir / f'range_classifier_{timestamp}.joblib')
            joblib.dump(self.price_regressor,
                       self.model_dir / f'price_regressor_{timestamp}.joblib')
            
            logger.info("Models trained and saved successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error training models: {str(e)}")
            return False
    
    def predict_price_range(self, features):
        """Predict price range for new products"""
        if not self.is_trained:
            logger.error("Models not trained yet")
            return None
            
        try:
            return self.range_classifier.predict(features)
        except Exception as e:
            logger.error(f"Error predicting price range: {str(e)}")
            return None
    
    def predict_price(self, features):
        """Predict exact price for new products"""
        if not self.is_trained:
            logger.error("Models not trained yet")
            return None
            
        try:
            return self.price_regressor.predict(features)
        except Exception as e:
            logger.error(f"Error predicting price: {str(e)}")
            return None
    
    def load_models(self, classifier_path, regressor_path):
        """Load pre-trained models"""
        try:
            self.range_classifier = joblib.load(classifier_path)
            self.price_regressor = joblib.load(regressor_path)
            self.is_trained = True
            logger.info("Models loaded successfully")
            return True
        except Exception as e:
            logger.error(f"Error loading models: {str(e)}")
            return False

    def get_feature_importance(self):
        """Get feature importance for both models"""
        if not self.is_trained:
            logger.error("Models not trained yet")
            return None
            
        try:
            importance_dict = {
                'price_range': {
                    'importance': self.range_classifier.feature_importances_,
                    'model': 'GradientBoosting'
                },
                'price': {
                    'importance': self.price_regressor.feature_importances_,
                    'model': 'RandomForest'
                }
            }
            return importance_dict
        except Exception as e:
            logger.error(f"Error getting feature importance: {str(e)}")
            return None
