"""
Script to create MySQL tables using SQLAlchemy models
"""
from models import create_tables

if __name__ == "__main__":
    create_tables()
    print("Tables created successfully!")
