"""
Debug environment variable loading.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

def main():
    # Get the project root directory
    project_root = Path(__file__).parent.parent.parent
    env_path = project_root / '.env'
    
    print(f"Project root: {project_root}")
    print(f"Looking for .env at: {env_path}")
    print(f"File exists: {env_path.exists()}")
    
    # Try to load the .env file
    load_dotenv(dotenv_path=env_path, verbose=True)
    
    # Print environment variables
    print("\nEnvironment variables:")
    for var in ['MYSQL_HOST', 'MYSQL_USER', 'MYSQL_PASSWORD', 'MYSQL_DATABASE', 'MYSQL_PORT']:
        print(f"{var}: {os.getenv(var, 'Not set')}")

if __name__ == "__main__":
    main()
