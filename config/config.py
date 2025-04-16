import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    # Database configurations
    MYSQL_USER = os.getenv("MYSQL_USER", "root")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
    MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
    MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")
    MYSQL_DB = os.getenv("MYSQL_DB", "price_intelligence")
    
    # MongoDB configurations
    MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
    MONGODB_DB = os.getenv("MONGODB_DB", "price_intelligence")
    
    # API configurations
    BESTBUY_API_KEY = os.getenv("BESTBUY_API_KEY")
    API_HOST = os.getenv("API_HOST", "0.0.0.0")
    API_PORT = int(os.getenv("API_PORT", "8000"))
    
    # Data pipeline configurations
    RAW_DATA_PATH = os.path.join("data", "raw")
    PROCESSED_DATA_PATH = os.path.join("data", "processed")
    
    # Feature flags
    ENABLE_CACHING = os.getenv("ENABLE_CACHING", "True").lower() == "true"
    DEBUG_MODE = os.getenv("DEBUG_MODE", "False").lower() == "true"
    
    # Monitoring and logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    @property
    def MYSQL_URI(self):
        from urllib.parse import quote_plus
        password = quote_plus(self.MYSQL_PASSWORD)
        return f"mysql+mysqlconnector://{self.MYSQL_USER}:{password}@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DB}?auth_plugin=mysql_native_password"

config = Config()
