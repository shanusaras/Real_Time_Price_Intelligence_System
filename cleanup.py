import os
import shutil
from pathlib import Path

def cleanup_project():
    base_dir = Path(__file__).parent
    api_dir = base_dir / 'api'
    
    # 1. Move contents of api/api to api/
    nested_api = api_dir / 'api'
    if nested_api.exists():
        print(f"Moving contents from {nested_api} to {api_dir}")
        for item in nested_api.glob('*'):
            dest = api_dir / item.name
            if dest.exists():
                if dest.is_dir():
                    shutil.rmtree(dest)
                else:
                    dest.unlink()
            shutil.move(str(item), str(api_dir))
        nested_api.rmdir()
    
    # 2. Remove empty __pycache__ directories
    print("Cleaning up __pycache__ directories...")
    for pycache in base_dir.rglob('__pycache__'):
        shutil.rmtree(pycache, ignore_errors=True)
    
    # 3. Clean up any .pyc files
    print("Removing .pyc files...")
    for pyc in base_dir.rglob('*.pyc'):
        pyc.unlink()
    
    # 4. Remove empty test files
    test_files_to_remove = [
        api_dir / 'test_connection.py',
        base_dir / 'test_connection.py',
        base_dir / 'test_db.py',
        base_dir / 'test_db_connection.py'
    ]
    
    for test_file in test_files_to_remove:
        if test_file.exists():
            print(f"Removing test file: {test_file}")
            test_file.unlink()
    
    print("\nCleanup complete! Project structure has been reorganized.")

if __name__ == "__main__":
    cleanup_project()
