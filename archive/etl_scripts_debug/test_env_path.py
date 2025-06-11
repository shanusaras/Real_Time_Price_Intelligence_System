"""
Test environment variables with explicit .env path.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

def main():
    # Get the project root directory (one level up from etl/)
    project_root = Path(__file__).parent.parent.parent
    env_path = project_root / '.env'
    
    print(f"Loading .env from: {env_path}")
    
    # Load environment variables from the specific path
    load_dotenv(dotenv_path=env_path)
    
    print("\nCurrent environment variables:")
    print(f"MYSQL_HOST: {os.getenv('MYSQL_HOST')}")
    print(f"MYSQL_USER: {os.getenv('MYSQL_USER')}")
    print(f"MYSQL_PASSWORD: {'*' * len(os.getenv('MYSQL_PASSWORD', ''))}")
    print(f"MYSQL_DATABASE: {os.getenv('MYSQL_DATABASE')}")
    print(f"MYSQL_PORT: {os.getenv('MYSQL_PORT', '3306')}")

if __name__ == "__main__":
    main()
