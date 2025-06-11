"""
Diagnose environment variable loading issues.
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

def print_section(title):
    print(f"\n{'='*80}")
    print(f"{title.upper()}")
    print(f"{'='*80}")

def main():
    # 1. Show Python and OS info
    print_section("System Information")
    print(f"Python: {sys.version}")
    print(f"Platform: {sys.platform}")
    print(f"Current Working Directory: {os.getcwd()}")
    
    # 2. Find and show all .env files
    print_section("Environment Files")
    project_root = Path(__file__).parent.parent.parent
    possible_env_files = [
        project_root / '.env',
        project_root / 'etl' / '.env',
        Path.home() / '.env',
    ]
    
    for env_file in possible_env_files:
        exists = "✅" if env_file.exists() else "❌"
        print(f"{exists} {env_file}")
    
    # 3. Load and show .env file contents
    env_path = project_root / '.env'
    if env_path.exists():
        print_section(f"Contents of {env_path}")
        try:
            with open(env_path, 'r') as f:
                print(f.read().strip())
        except Exception as e:
            print(f"Error reading .env file: {e}")
    
    # 4. Show current environment variables
    print_section("Current Environment Variables")
    env_vars = [
        'MYSQL_HOST', 'MYSQL_USER', 'MYSQL_PASSWORD',
        'MYSQL_DATABASE', 'MYSQL_PORT'
    ]
    
    for var in env_vars:
        value = os.getenv(var, 'Not set')
        print(f"{var}: {value}")
    
    # 5. Test database connection
    print_section("Database Connection Test")
    try:
        from sqlalchemy import create_engine, text
        from urllib.parse import quote_plus
        
        db_config = {
            'host': os.getenv('MYSQL_HOST'),
            'user': os.getenv('MYSQL_USER'),
            'password': os.getenv('MYSQL_PASSWORD'),
            'database': os.getenv('MYSQL_DATABASE'),
            'port': os.getenv('MYSQL_PORT', '3306')
        }
        
        print(f"Attempting to connect to database: {db_config['database']}")
        
        # Create connection string
        encoded_password = quote_plus(db_config['password'] or '')
        connection_string = f"mysql+pymysql://{db_config['user']}:{encoded_password}@{db_config['host']}:{db_config['port']}/{db_config['database']}"
        
        # Test connection
        engine = create_engine(connection_string)
        with engine.connect() as connection:
            print("✅ Successfully connected to the database!")
            
            # Get database name
            result = connection.execute(text("SELECT DATABASE()"))
            db_name = result.scalar()
            print(f"Connected to database: {db_name}")
            
    except Exception as e:
        print(f"❌ Database connection failed: {e}")

if __name__ == "__main__":
    main()
