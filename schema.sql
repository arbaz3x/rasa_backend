-- schema.sql (PostgreSQL)

-- Table for chatbot conversations
CREATE TABLE IF NOT EXISTS conversations (
    id SERIAL PRIMARY KEY,
    user_id TEXT,
    session_id TEXT,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    user_message TEXT,
    bot_response TEXT,
    intent TEXT,
    entities JSONB  -- Store as JSON, e.g., {"product": "jeans"}
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

-- Table for FAQs
CREATE TABLE IF NOT EXISTS faqs (
    id SERIAL PRIMARY KEY,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    category TEXT
);
-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE
);

-- Carts table
CREATE TABLE carts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Cart items table
CREATE TABLE cart_items (
    id SERIAL PRIMARY KEY,
    cart_id INTEGER REFERENCES carts(id),
    product_id INTEGER REFERENCES products(id),
    quantity INTEGER DEFAULT 1
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


