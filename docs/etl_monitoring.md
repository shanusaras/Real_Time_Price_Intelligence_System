# ETL Monitoring and Alerts System

## Overview
The ETL monitoring system provides comprehensive tracking of data quality, processing performance, and system health. It includes:

### 1. Data Quality Metrics
- **Total Records Processed**: Number of records processed in each run
- **Null Values Analysis**: 
  - Total count of null values
  - Percentage of null values in the dataset
- **Price Statistics**: 
  - Minimum price
  - Maximum price
  - Average price
  - Standard deviation of prices
- **Category Distribution**: Count of products per category
- **Processing Time**: Time taken for ETL process

### 2. Alert System
The system generates alerts for:
1. **Performance Issues**:
   - Processing time exceeding 60 seconds
   
2. **Data Quality Issues**:
   - More than 5% null values in the dataset
   - Price values outside the expected range (0-1,000,000)

### 3. Monitoring Output
The system generates JSON files in the `monitoring/` directory with the following format:

```json
{
    "total_records": 13966,
    "null_values": {
        "count": 0,
        "percentage": 0.0
    },
    "price_statistics": {
        "min": 10.99,
        "max": 99999.99,
        "mean": 2500.50,
        "std_dev": 1500.25
    },
    "category_distribution": {
        "electronics": 3000,
        "fashion": 2500,
        "home": 2000,
        "...
    },
    "processing_time": 120.50
}
```

### 4. Usage
The monitoring system is automatically triggered with each ETL run and:
1. Logs metrics to JSON files
2. Generates alerts in the logs if thresholds are exceeded
3. Provides real-time performance tracking

### 5. Benefits
- Early detection of data quality issues
- Performance monitoring and optimization
- Historical tracking of ETL runs
- Automated alerting for potential problems
- Better understanding of data distribution

This monitoring system helps ensure the reliability and quality of the ETL process, providing valuable insights for system optimization and troubleshooting.
