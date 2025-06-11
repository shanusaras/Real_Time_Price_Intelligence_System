"""
Create the database if it doesn't exist.
"""
import pymysql
from dotenv import load_dotenv
import os
from pathlib import Path

# Load environment variables
project_root = Path(__file__).parent.parent.parent
load_dotenv(dotenv_path=project_root / '.env')

def create_database():
    try:
        # Connect without specifying a database
        connection = pymysql.connect(
            host=os.getenv('MYSQL_HOST'),
            user=os.getenv('MYSQL_USER'),
            password=os.getenv('MYSQL_PASSWORD'),
            port=int(os.getenv('MYSQL_PORT', '3306')),
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        
        db_name = os.getenv('MYSQL_DATABASE')
        
        with connection.cursor() as cursor:
            # Create database if it doesn't exist
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
            print(f"✅ Database '{db_name}' created or already exists")
            
            # Show all databases for verification
            cursor.execute("SHOW DATABASES;")
            print("\nAvailable databases:")
            for db in cursor.fetchall():
                print(f"- {db['Database']}")
                
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        if 'connection' in locals() and connection.open:
            connection.close()

if __name__ == "__main__":
    print(f"Attempting to create database: {os.getenv('MYSQL_DATABASE')}")
    create_database()
