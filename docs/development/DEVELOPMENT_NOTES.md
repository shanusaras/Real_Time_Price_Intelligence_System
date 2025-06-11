# Development Notes: Database Connection Setup

## Overview
This document outlines the challenges faced and solutions implemented during the database connection setup for the ETL pipeline.

## Challenges

### 1. Environment Variable Management
- **Issue**: System environment variables were overriding local `.env` file settings
- **Symptoms**: Database name kept defaulting to `price_intelligence_v2` despite `.env` updates
- **Root Cause**: System-wide environment variables taking precedence

### 2. Special Character Handling
- **Issue**: Special characters in MySQL password (special symbols) caused connection failures
- **Symptoms**: Malformed connection strings and authentication errors
- **Example**: `[REDACTED]` needed URL encoding

## Solutions Implemented

### 1. Robust Connection Handling
- Added URL encoding for database passwords using `urllib.parse.quote_plus()`
- Implemented explicit environment variable loading with specific paths
- Created validation for required environment variables

### 2. Database Connection Utilities
- `force_database.py`: Ensures consistent database naming
- `test_db_connection.py`: Validates database connectivity with detailed error reporting
- `setup_db.py`: Handles table creation with proper environment variable handling

## Key Code Snippets

### URL Encoding for Passwords
```python
from urllib.parse import quote_plus
encoded_password = quote_plus(os.getenv('MYSQL_PASSWORD', ''))
```

### Forcing Database Name
```python
# In force_database.py
os.environ['MYSQL_DATABASE'] = 'price_intelligence'
```

## Testing

### Verifying the Setup
1. Run the test connection script:
   ```bash
   python -m etl.scripts.test_db_connection
   ```

2. Expected output should show successful connection to `price_intelligence`

## Future Improvements
- Add connection pooling for better performance
- Implement retry logic for transient failures
- Add more comprehensive error handling and logging
