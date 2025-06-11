import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', 3306)),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'price_intelligence')
}

# API Configuration
API_CONFIG = {
    'title': 'Price Intelligence API',
    'description': 'API for accessing and analyzing product pricing data from Jumia',
    'version': '1.0.0',
    'debug': os.getenv('DEBUG', 'False').lower() in ('true', '1', 't'),
    'rate_limit': {
        'max_requests': int(os.getenv('RATE_LIMIT_MAX_REQUESTS', 100)),
        'window_seconds': int(os.getenv('RATE_LIMIT_WINDOW_SECONDS', 60))
    }
}
