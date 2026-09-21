-- ============================================================
-- PETFLOW - ANÁLISE DE CLIENTES
-- ============================================================

-- 1. Distribuição dos clientes por segmento RFM

SELECT
    customer_segment,
    COUNT(*) AS customers,
    ROUND(
        100.0 * COUNT(*) / SUM(COUNT(*)) OVER (),
        2
    ) AS percentage
FROM warehouse.customer_rfm
GROUP BY customer_segment
ORDER BY customers DESC;


-- 2. Perfil médio de cada segmento

SELECT
    customer_segment,
    COUNT(*) AS customers,
    ROUND(AVG(total_orders), 2) AS avg_orders,
    ROUND(AVG(total_spent), 2) AS avg_spent,
    ROUND(AVG(average_order_value), 2) AS avg_order_value,
    ROUND(AVG(days_since_last_purchase), 2) AS avg_recency
FROM warehouse.customer_rfm
GROUP BY customer_segment
ORDER BY avg_spent DESC;


-- 3. Clientes de maior valor

SELECT
    customer_unique_id,
    customer_city,
    customer_state,
    total_orders,
    total_spent,
    average_order_value,
    days_since_last_purchase,
    customer_segment
FROM warehouse.customer_rfm
ORDER BY total_spent DESC
LIMIT 20;