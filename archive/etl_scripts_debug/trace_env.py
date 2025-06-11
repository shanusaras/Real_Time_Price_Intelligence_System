"""
Trace environment variable loading.
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv, find_dotenv

def print_env_file(env_path):
    """Print the contents of an environment file if it exists."""
    print(f"\nContents of {env_path}:")
    print("-" * 50)
    try:
        with open(env_path, 'r') as f:
            print(f.read())
    except Exception as e:
        print(f"Could not read file: {e}")
    print("-" * 50)

def main():
    # Find all .env files
    project_root = Path(__file__).parent.parent.parent
    possible_env_files = [
        project_root / '.env',
        project_root / 'etl' / '.env',
        Path.home() / '.env',
    ]
    
    print("Searching for .env files in:")
    for env_file in possible_env_files:
        print(f"- {env_file} (exists: {env_file.exists()})")
    
    # Print contents of all found .env files
    for env_file in possible_env_files:
        if env_file.exists():
            print_env_file(env_file)
    
    # Show what dotenv finds
    print("\nUsing find_dotenv():")
    env_path = find_dotenv(usecwd=True)
    print(f"Found .env at: {env_path}")
    
    if env_path:
        print_env_file(env_path)
    
    # Load environment and show values
    print("\nCurrent environment variables:")
    for var in ['MYSQL_HOST', 'MYSQL_USER', 'MYSQL_PASSWORD', 'MYSQL_DATABASE', 'MYSQL_PORT']:
        print(f"{var}: {os.getenv(var, 'Not set')}")

if __name__ == "__main__":
    main()
