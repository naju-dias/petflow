-- ============================================================
-- PETFLOW
-- STAGING TABLES
-- ============================================================

-- ============================================================
-- CUSTOMERS
-- ============================================================

CREATE TABLE IF NOT EXISTS staging.customers (
    customer_id VARCHAR(32) PRIMARY KEY,
    customer_unique_id VARCHAR(32) NOT NULL,
    customer_zip_code_prefix INTEGER,
    customer_city VARCHAR(100),
    customer_state VARCHAR(2)
);


-- ============================================================
-- ORDERS
-- ============================================================

CREATE TABLE IF NOT EXISTS staging.orders (
    order_id VARCHAR(32) PRIMARY KEY,
    customer_id VARCHAR(32) NOT NULL,
    order_status VARCHAR(30) NOT NULL,

    order_purchase_timestamp TIMESTAMP,
    order_approved_at TIMESTAMP,
    order_delivered_carrier_date TIMESTAMP,
    order_delivered_customer_date TIMESTAMP,
    order_estimated_delivery_date TIMESTAMP
);


-- ============================================================
-- ORDER ITEMS
-- ============================================================

CREATE TABLE IF NOT EXISTS staging.order_items (
    order_id VARCHAR(32) NOT NULL,
    order_item_id INTEGER NOT NULL,

    product_id VARCHAR(32) NOT NULL,
    seller_id VARCHAR(32) NOT NULL,

    shipping_limit_date TIMESTAMP,

    price NUMERIC(12,2),
    freight_value NUMERIC(12,2),

    PRIMARY KEY (order_id, order_item_id)
);


-- ============================================================
-- PAYMENTS
-- ============================================================

CREATE TABLE IF NOT EXISTS staging.order_payments (
    order_id VARCHAR(32) NOT NULL,
    payment_sequential INTEGER NOT NULL,

    payment_type VARCHAR(30),
    payment_installments INTEGER,
    payment_value NUMERIC(12,2),

    PRIMARY KEY (
        order_id,
        payment_sequential
    )
);


-- ============================================================
-- REVIEWS
-- ============================================================

CREATE TABLE IF NOT EXISTS staging.order_reviews (
    review_id VARCHAR(32) PRIMARY KEY,

    order_id VARCHAR(32) NOT NULL,

    review_score INTEGER,

    review_comment_title TEXT,
    review_comment_message TEXT,

    review_creation_date TIMESTAMP,
    review_answer_timestamp TIMESTAMP
);


-- ============================================================
-- PRODUCTS
-- ============================================================

CREATE TABLE IF NOT EXISTS staging.products (
    product_id VARCHAR(32) PRIMARY KEY,

    product_category_name VARCHAR(100),

    product_name_length INTEGER,
    product_description_length INTEGER,

    product_photos_qty INTEGER,

    product_weight_g NUMERIC(12,2),

    product_length_cm NUMERIC(12,2),
    product_height_cm NUMERIC(12,2),
    product_width_cm NUMERIC(12,2)
);


-- ============================================================
-- SELLERS
-- ============================================================

CREATE TABLE IF NOT EXISTS staging.sellers (
    seller_id VARCHAR(32) PRIMARY KEY,

    seller_zip_code_prefix INTEGER,

    seller_city VARCHAR(100),
    seller_state VARCHAR(2)
);