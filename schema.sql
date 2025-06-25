-- schema.sql (PostgreSQL)

-- Table for chatbot conversations
CREATE TABLE users (
  user_id TEXT PRIMARY KEY,
  -- other user fields
);

CREATE TABLE IF NOT EXISTS conversations (
    id SERIAL PRIMARY KEY,
    user_id TEXT,
    session_id TEXT,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    user_message TEXT,
    bot_response TEXT,
    intent TEXT,
    entities JSONB 
);

-- Table for products
CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT,
    description TEXT,
    price REAL,
    color TEXT,
    size TEXT,
    stock INTEGER,
    image_url TEXT
);


CREATE TABLE orders (
    order_id VARCHAR(255) PRIMARY KEY,
    user_id VARCHAR(255),
    order_date DATE,
    status VARCHAR(50)
);

CREATE TABLE order_items (
    order_id VARCHAR(255) REFERENCES orders(order_id),
    product_name VARCHAR(255),
    price DECIMAL(10,2),
    quantity INTEGER
);


