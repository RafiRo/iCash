CREATE TABLE IF NOT EXISTS products_list (
    id SERIAL PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    unit_price REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS supermarket (
	id SERIAL PRIMARY KEY,
        supermarket_id VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS app_user (
	id SERIAL PRIMARY KEY,
        user_id VARCHAR(36) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS purchases (
    id SERIAL PRIMARY KEY,
    supermarket_id VARCHAR(255) REFERENCES supermarket(supermarket_id),
    "timestamp" TIMESTAMP(6) NOT NULL DEFAULT CURRENT_DATE,
    user_id VARCHAR(36) REFERENCES app_user(user_id),
    item_list TEXT,
    total_amount REAL DEFAULT 0.0
);

