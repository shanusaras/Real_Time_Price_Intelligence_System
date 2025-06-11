"""
Force environment variables to specific values.
"""
import os
import sys
from pathlib import Path
from urllib.parse import quote_plus

# Get the project root
project_root = Path(__file__).parent.parent.parent

# Force the environment variables
os.environ['MYSQL_HOST'] = '127.0.0.1'
os.environ['MYSQL_USER'] = 'root'
# URL encode the password to handle special characters
os.environ['MYSQL_PASSWORD'] = quote_plus('smartie@123.')
os.environ['MYSQL_DATABASE'] = 'price_intelligence'  # Force this value
os.environ['MYSQL_PORT'] = '3306'

# Now import and run the database test
from etl.scripts.test_db_connection import test_connection

if __name__ == "__main__":
    print("Forcing environment variables...")
    test_connection()
