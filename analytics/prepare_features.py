from ml_preprocessor import MLPreprocessor
from backend.models.db_manager import DatabaseManager
import logging
import sys
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'logs/ml_prep_{datetime.now().strftime("%Y%m%d")}.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

def prepare_ml_features(lookback_days=30):
    """
    Prepare ML features for all products
    Args:
        lookback_days: Number of days of historical data to consider
    """
    try:
        # Initialize database connection
        db_manager = DatabaseManager()
        
        with db_manager.get_session() as session:
            # Initialize preprocessor
            preprocessor = MLPreprocessor(session)
            
            # Prepare features
            logger.info(f"Starting feature preparation with {lookback_days} days lookback")
            preprocessor.prepare_features(lookback_days=lookback_days)
            
            # Get training data to verify
            X, y = preprocessor.get_training_data()
            if X is not None and y is not None:
                logger.info(f"Successfully prepared features for {len(X)} products")
                logger.info(f"Feature matrix shape: {X.shape}")
                logger.info(f"Unique price ranges: {set(y)}")
            else:
                logger.warning("No valid training data generated")
            
            return True
            
    except Exception as e:
        logger.error(f"Error during feature preparation: {str(e)}")
        return False

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Prepare ML features for price intelligence")
    parser.add_argument("--lookback", type=int, default=30,
                       help="Number of days of historical data to consider")
    
    args = parser.parse_args()
    
    success = prepare_ml_features(args.lookback)
    sys.exit(0 if success else 1)
