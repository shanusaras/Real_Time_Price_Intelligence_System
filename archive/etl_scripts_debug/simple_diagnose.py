"""
Simple environment variable diagnosis script.
"""
import os
import sys
from pathlib import Path

def main():
    print("=== Environment Variable Diagnosis ===\n")
    
    # 1. Show current working directory
    print(f"Current Working Directory: {os.getcwd()}")
    
    # 2. Show .env file path
    env_path = Path(__file__).parent.parent.parent / '.env'
    print(f"\nLooking for .env at: {env_path}")
    
    # 3. Try to read and show .env contents
    try:
        with open(env_path, 'r') as f:
            print("\nContents of .env:")
            print("-" * 50)
            print(f.read())
            print("-" * 50)
    except Exception as e:
        print(f"\nError reading .env file: {e}")
    
    # 4. Show relevant environment variables
    print("\nEnvironment Variables:")
    for var in ['MYSQL_HOST', 'MYSQL_USER', 'MYSQL_PASSWORD', 'MYSQL_DATABASE', 'MYSQL_PORT']:
        value = os.getenv(var, 'Not set')
        print(f"{var}: {value}")

if __name__ == "__main__":
    main()
