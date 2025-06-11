"""
Test database connection by reading .env file directly.
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from urllib.parse import quote_plus
from sqlalchemy import create_engine, text

def main():
    # Get the absolute path to the .env file
    env_path = Path(__file__).parent.parent.parent / '.env'
    print(f"Reading .env from: {env_path}")
    
    # Read the .env file directly
    if not env_path.exists():
        print(f"❌ Error: {env_path} does not exist")
        return
    
    # Print the contents of the .env file
    print("\nContents of .env file:")
    print("-" * 50)
    with open(env_path, 'r') as f:
        print(f.read())
    print("-" * 50)
    
    # Load environment variables directly from the file
    load_dotenv(dotenv_path=env_path, override=True)
    
    # Get database configuration
    db_config = {
        'host': os.getenv('MYSQL_HOST'),
        'user': os.getenv('MYSQL_USER'),
        'password': os.getenv('MYSQL_PASSWORD'),
        'database': os.getenv('MYSQL_DATABASE'),
        'port': os.getenv('MYSQL_PORT', '3306')
    }
    
    print("\nUsing database configuration:")
    print(f"Host: {db_config['host']}")
    print(f"Database: {db_config['database']}")
    print(f"Port: {db_config['port']}")
    
    try:
        # URL encode the password
        encoded_password = quote_plus(db_config['password'])
        
        # Create connection string
        connection_string = f"mysql+pymysql://{db_config['user']}:{encoded_password}@{db_config['host']}:{db_config['port']}/{db_config['database']}"
        
        # Test connection
        engine = create_engine(connection_string)
        with engine.connect() as connection:
            print("\n✅ Successfully connected to the database!")
            
            # Simple test query
            result = connection.execute(text("SELECT 1"))
            row = result.fetchone()
            print(f"Test query result: {row[0]}")
            
            # Get current database
            db_result = connection.execute(text("SELECT DATABASE()"))
            db_name = db_result.scalar()
            print(f"Connected to database: {db_name}")
            
    except Exception as e:
        print(f"\n❌ Failed to connect to the database: {e}")
        print("\nTroubleshooting steps:")
        print("1. Make sure MySQL server is running")
        print("2. Verify your MySQL credentials in the .env file")
        print("3. Ensure the database exists")
        print(f"4. Check if user has permissions on database: {db_config['database']}")

if __name__ == "__main__":
    main()
