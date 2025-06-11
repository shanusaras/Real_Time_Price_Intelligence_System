# Debug Scripts Archive

This directory contains debugging and diagnostic scripts used during the development of the ETL pipeline. These scripts were created to help troubleshoot environment variable and database connection issues.

## Contents

### Environment Debugging
- `debug_env.py` - Debugs environment variable loading
- `diagnose_env.py` - Comprehensive environment diagnosis tool
- `direct_env_test.py` - Tests direct environment loading
- `force_env.py` - Forces specific environment variables
- `simple_diagnose.py` - Lightweight environment checker
- `test_env_path.py` - Tests environment file paths
- `trace_env.py` - Traces environment variable loading

### Database Utilities
- `create_db.py` - Creates the MySQL database

## Usage

These scripts are not required for normal operation of the application. They were used during development to diagnose and fix environment-specific issues.

## Notes

- These scripts are provided for reference and debugging purposes.
- The final production code handles these cases in a more robust way.
- Environment-specific configurations have been moved to the main `.env` file.

## Production Solution

The final solution for handling database connections is implemented in:
- `etl/scripts/test_db_connection.py`
- `etl/scripts/force_database.py`
- `etl/scripts/setup_db.py`
