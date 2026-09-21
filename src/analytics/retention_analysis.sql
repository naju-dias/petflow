-- ============================================================
-- PETFLOW - ANÁLISE DE RETENÇÃO
-- ============================================================


-- 1. Clientes de uma compra vs recorrentes

SELECT
    CASE
        WHEN total_orders = 1 THEN 'one_time'
        ELSE 'repeat'
    END AS customer_type,
    COUNT(*) AS customers,
    ROUND(
        100.0 * COUNT(*) / SUM(COUNT(*)) OVER (),
        2
    ) AS percentage
FROM warehouse.customer_analytics
GROUP BY 1
ORDER BY customers DESC;


-- 2. Distribuição de frequência de compra

SELECT
    total_orders,
    COUNT(*) AS customers
FROM warehouse.customer_analytics
GROUP BY total_orders
ORDER BY total_orders;


-- 3. Clientes potencialmente em risco

SELECT
    customer_unique_id,
    customer_city,
    customer_state,
    total_orders,
    total_spent,
    days_since_last_purchase,
    rfm_score,
    customer_segment
FROM warehouse.customer_rfm
WHERE customer_segment = 'at_risk'
ORDER BY total_spent DESC
LIMIT 100;


-- 4. Clientes inativos

SELECT
    customer_unique_id,
    customer_city,
    customer_state,
    total_orders,
    total_spent,
    days_since_last_purchase,
    customer_segment
FROM warehouse.customer_rfm
WHERE customer_segment = 'inactive'
ORDER BY total_spent DESC
LIMIT 100;