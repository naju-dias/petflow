-- ============================================================
-- PETFLOW
-- DATA WAREHOUSE
-- ============================================================


-- ============================================================
-- DIM CUSTOMER
-- ============================================================

CREATE TABLE IF NOT EXISTS warehouse.dim_customer (

    customer_key BIGSERIAL PRIMARY KEY,

    customer_unique_id VARCHAR(32) NOT NULL UNIQUE,

    customer_city VARCHAR(100),

    customer_state VARCHAR(2),

    customer_zip_code_prefix INTEGER
);

ALTER TABLE warehouse.dim_customer
ADD COLUMN customer_id VARCHAR(32);

-- ============================================================
-- DIM PRODUCT
-- ============================================================

CREATE TABLE IF NOT EXISTS warehouse.dim_product (

    product_key BIGSERIAL PRIMARY KEY,

    product_id VARCHAR(32) NOT NULL UNIQUE,

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
-- DIM SELLER
-- ============================================================

CREATE TABLE IF NOT EXISTS warehouse.dim_seller (

    seller_key BIGSERIAL PRIMARY KEY,

    seller_id VARCHAR(32) NOT NULL UNIQUE,

    seller_city VARCHAR(100),

    seller_state VARCHAR(2),

    seller_zip_code_prefix INTEGER

);

-- ============================================================
-- DIM DATE
-- ============================================================

CREATE TABLE IF NOT EXISTS warehouse.dim_date (

    date_key INTEGER PRIMARY KEY,

    full_date DATE NOT NULL UNIQUE,

    year INTEGER NOT NULL,

    quarter INTEGER NOT NULL,

    month INTEGER NOT NULL,

    month_name VARCHAR(20) NOT NULL,

    week INTEGER NOT NULL,

    day INTEGER NOT NULL,

    day_of_week INTEGER NOT NULL,

    day_name VARCHAR(20) NOT NULL,

    is_weekend BOOLEAN NOT NULL

);

-- ============================================================
-- FACT ORDER
-- Granularidade: 1 linha por pedido
-- ============================================================

CREATE TABLE IF NOT EXISTS warehouse.fact_order (

    order_key BIGSERIAL PRIMARY KEY,

    order_id VARCHAR(32) NOT NULL UNIQUE,

    customer_key BIGINT NOT NULL,

    order_date_key INTEGER NOT NULL,

    order_status VARCHAR(30) NOT NULL,

    order_purchase_timestamp TIMESTAMP,

    order_approved_at TIMESTAMP,

    order_delivered_carrier_date TIMESTAMP,

    order_delivered_customer_date TIMESTAMP,

    order_estimated_delivery_date TIMESTAMP,

    order_product_value NUMERIC(12,2),

    order_freight_value NUMERIC(12,2),

    order_value NUMERIC(12,2)

);

-- ============================================================
-- FACT ORDER ITEM
-- Granularidade: 1 linha por item de pedido
-- ============================================================

CREATE TABLE IF NOT EXISTS warehouse.fact_order_item (

    order_item_key BIGSERIAL PRIMARY KEY,

    order_id VARCHAR(32) NOT NULL,

    order_item_id INTEGER NOT NULL,

    product_key BIGINT NOT NULL,

    seller_key BIGINT NOT NULL,

    shipping_limit_date TIMESTAMP,

    price NUMERIC(12,2),

    freight_value NUMERIC(12,2),

    UNIQUE (
        order_id,
        order_item_id
    )

);

-- ============================================================
-- FOREIGN KEYS
-- ============================================================


ALTER TABLE warehouse.fact_order

ADD CONSTRAINT fk_fact_order_customer

FOREIGN KEY (customer_key)

REFERENCES warehouse.dim_customer(customer_key);


ALTER TABLE warehouse.fact_order

ADD CONSTRAINT fk_fact_order_date

FOREIGN KEY (order_date_key)

REFERENCES warehouse.dim_date(date_key);


ALTER TABLE warehouse.fact_order_item

ADD CONSTRAINT fk_fact_order_item_product

FOREIGN KEY (product_key)

REFERENCES warehouse.dim_product(product_key);


ALTER TABLE warehouse.fact_order_item

ADD CONSTRAINT fk_fact_order_item_seller

FOREIGN KEY (seller_key)

REFERENCES warehouse.dim_seller(seller_key);