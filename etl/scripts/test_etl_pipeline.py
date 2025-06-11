"""
Test script for the ETL pipeline with a sample of the scraped data.
"""
import json
import sys
from pathlib import Path
from datetime import datetime

# Add the project root to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from etl.src.etl_pipeline import ETLPipeline

def test_etl_with_sample_data(input_file: str, sample_size: int = 10):
    """
    Test the ETL pipeline with a sample of the scraped data.
    
    Args:
        input_file: Path to the input JSON file
        sample_size: Number of items to sample from the input file
    """
    print(f"Testing ETL pipeline with {sample_size} sample records...")
    
    # Create a sample file with the first N records
    sample_file = Path("etl/data/sample_data.json")
    sample_file.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        # Read the input file and extract a sample
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        # Ensure we don't exceed the available data
        sample_size = min(sample_size, len(data))
        sample_data = data[:sample_size]
        
        # Save the sample to a file
        with open(sample_file, 'w', encoding='utf-8') as f:
            json.dump(sample_data, f, indent=2)
            
        print(f"Created sample file with {len(sample_data)} records at: {sample_file}")
        
        # Initialize and run the ETL pipeline
        pipeline = ETLPipeline(str(sample_file))
        stats = pipeline.run()
        
        print("\nETL Pipeline Results:")
        print(f"Status: {stats['status'].upper()}")
        print(f"Duration: {stats['duration_seconds']:.2f} seconds")
        print(f"Extracted: {stats['extracted']}")
        print(f"Cleaned: {stats['cleaned']}")
        print(f"Valid: {stats['valid']}")
        print(f"Invalid: {stats['invalid']}")
        print(f"Loaded: {stats['loaded']}")
        print(f"Errors: {stats['errors']}")
        
        return stats
        
    except Exception as e:
        print(f"Error during ETL test: {e}")
        raise
    finally:
        # Clean up the sample file
        if sample_file.exists():
            sample_file.unlink()

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Test the ETL pipeline with sample data')
    parser.add_argument('input_file', type=str, help='Path to the input JSON file')
    parser.add_argument('--sample-size', type=int, default=10, 
                       help='Number of records to sample (default: 10)')
    
    args = parser.parse_args()
    
    test_etl_with_sample_data(
        input_file=args.input_file,
        sample_size=args.sample_size
    )
