-- ============================================================
-- PETFLOW - ANÁLISE DE VENDAS
-- ============================================================


-- 1. Evolução mensal dos pedidos e receita

SELECT
    DATE_TRUNC('month', order_purchase_timestamp)::date AS month,
    COUNT(DISTINCT order_id) AS orders,
    ROUND(SUM(order_value), 2) AS revenue,
    ROUND(AVG(order_value), 2) AS average_order_value
FROM warehouse.fact_order
WHERE order_status = 'delivered'
GROUP BY 1
ORDER BY 1;


-- 2. Receita por estado

SELECT
    c.customer_state,
    COUNT(DISTINCT f.order_id) AS orders,
    ROUND(SUM(f.order_value), 2) AS revenue,
    ROUND(AVG(f.order_value), 2) AS average_order_value
FROM warehouse.fact_order f
JOIN warehouse.dim_customer c
    ON f.customer_key = c.customer_key
WHERE f.order_status = 'delivered'
GROUP BY c.customer_state
ORDER BY revenue DESC;


-- 3. Categorias de produtos com maior faturamento

SELECT
    p.product_category_name,
    COUNT(DISTINCT oi.order_id) AS orders,
    ROUND(SUM(oi.price), 2) AS product_revenue
FROM warehouse.fact_order_item oi
JOIN warehouse.dim_product p
    ON oi.product_key = p.product_key
GROUP BY p.product_category_name
ORDER BY product_revenue DESC
LIMIT 20;