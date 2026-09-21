-- ============================================================
-- PETFLOW
-- CUSTOMER ANALYTICS
-- ============================================================

DROP VIEW IF EXISTS warehouse.customer_analytics;

CREATE OR REPLACE VIEW warehouse.customer_analytics AS

WITH delivered_orders AS (

    SELECT
        fo.order_id,
        fo.customer_key,
        fo.order_purchase_timestamp,
        fo.order_value

    FROM warehouse.fact_order fo

    WHERE fo.order_status = 'delivered'

      -- Data de corte utilizada na análise exploratória.
      AND fo.order_purchase_timestamp
          <= TIMESTAMP '2018-08-31 23:59:59'
),

customer_behavior AS (

    SELECT

        dc.customer_key,

        dc.customer_unique_id,

        dc.customer_city,

        dc.customer_state,

        MIN(d.order_purchase_timestamp)
            AS first_purchase_date,

        MAX(d.order_purchase_timestamp)
            AS last_purchase_date,

        COUNT(DISTINCT d.order_id)
            AS total_orders,

        SUM(d.order_value)
            AS total_spent,

        AVG(d.order_value)
            AS average_order_value

    FROM delivered_orders d

    INNER JOIN warehouse.dim_customer dc
        ON d.customer_key = dc.customer_key

    GROUP BY

        dc.customer_key,
        dc.customer_unique_id,
        dc.customer_city,
        dc.customer_state
)

SELECT

    customer_key,

    customer_unique_id,

    customer_city,

    customer_state,

    first_purchase_date,

    last_purchase_date,

    total_orders,

    ROUND(total_spent, 2)
        AS total_spent,

    ROUND(average_order_value, 2)
        AS average_order_value,

    ROUND(
        EXTRACT(
            EPOCH FROM (
                TIMESTAMP '2018-08-31 23:59:59'
                - last_purchase_date
            )
        ) / 86400,
        2
    ) AS days_since_last_purchase,

    CASE
        WHEN total_orders >= 2
            THEN 'repeat'
        ELSE 'one_time'
    END AS customer_type

FROM customer_behavior;