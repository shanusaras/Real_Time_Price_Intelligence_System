# ETL Validation Architecture

This document outlines the validation strategy used in the Price Intelligence ETL pipeline, explaining the different layers of validation and their purposes.

## Validation Layers

### 1. Transformers Layer (During ETL)
**Location**: `etl/src/transformers/`
**Files**: 
- `cleaner.py` - Cleans and standardizes data
- `validator.py` - Validates individual records

**Purpose**:
- Ensure data quality at the point of transformation
- Handle malformed or invalid records
- Enforce data types and required fields

**Example Checks**:
```python
# validator.py
def validate_product(product):
    if not product.get('name'):
        return False, "Missing product name"
    if not isinstance(product.get('price'), (int, float)):
        return False, "Invalid price format"
    return True, ""
```

### 2. Data Validation Script (Post-ETL)
**Location**: `etl/utils/data_validation.py`

**Purpose**:
- Verify data was loaded correctly into the database
- Check referential integrity
- Validate business rules across the entire dataset
- Monitor data quality over time

**Example Checks**:
```python
# Check referential integrity
missing_prices = session.query(Product).outerjoin(Price).filter(Price.id.is_(None)).count()

# Validate category distribution
category_counts = session.query(
    Category.name, 
    func.count(Product.id)
).join(Product).group_by(Category.name).all()
```

## Key Differences

| Aspect          | Transformers Validation | Data Validation Script |
|-----------------|-------------------------|------------------------|
| **When**       | During ETL process      | After ETL completes    |
| **Scope**      | Single record          | Entire dataset         |
| **Goal**       | Data cleaning          | Data integrity         |
| **Action**     | Fix/flag bad data      | Verify system health   |
| **Frequency**  | Every ETL run          | Scheduled/Monitoring   |

## When to Use Each

### Use Transformers When:
- Validating individual field formats
- Ensuring required fields exist
- Standardizing data formats
- Handling edge cases in raw data

### Use Data Validation When:
- Verifying data relationships
- Monitoring data quality trends
- Validating business rules
- Generating data quality reports

## Real-world Analogy

- **Transformers**: Like a bouncer checking IDs at a club (individual checks)
- **Data Validation**: Like the club owner reviewing the night's attendance and sales (big picture analysis)

## Running Validations

### Transformers Validation
Happens automatically during ETL runs:
```bash
python -m etl.src.etl_pipeline input_file.json
```

### Data Validation
Can be run manually or scheduled:
```bash
python -m etl.utils.data_validation
```

## Monitoring

Validation results are logged to:
- ETL logs in `etl/output/`
- Data quality metrics in `etl/monitoring/`

## Adding New Validations

1. **For record-level validations**: Add to `validator.py`
2. **For system-level validations**: Add to `data_validation.py`
3. **Update this document** with any new validation patterns
