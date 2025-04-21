-- Table schema for raw and cleaned product data

CREATE TABLE IF NOT EXISTS products (
    id VARCHAR(64) PRIMARY KEY,
    product_name TEXT,
    brands TEXT,
    categories TEXT,
    scraped_category VARCHAR(64),
    price DECIMAL(10,2),
    quantity VARCHAR(32),
    image_url TEXT,
    last_scraped DATETIME
);

CREATE TABLE IF NOT EXISTS products_clean (
    id VARCHAR(64) PRIMARY KEY,
    product_name VARCHAR(255),
    brand VARCHAR(128),
    category VARCHAR(64),
    scraped_category VARCHAR(64),
    price DECIMAL(10,2),
    unit_price DECIMAL(10,2),
    quantity VARCHAR(32),
    last_scraped DATETIME
);
