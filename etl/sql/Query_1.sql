SHOW DATABASES LIKE 'price_intelligence';
SHOW tables;

-- since we already have price_intelligene database👇
CREATE DATABASE price_intelligence_v2;
USE price_intelligence_v2;

ALTER TABLE products MODIFY COLUMN name TEXT;

DESC products;
SELECT DISTINCT brand FROM products;

SELECT * FROM price_history WHERE discount_pct > 0 LIMIT 10;