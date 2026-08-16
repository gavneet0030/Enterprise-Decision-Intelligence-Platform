-- ============================================================
-- EDIP BUSINESS METRICS LAYER
-- ============================================================


-- ============================================================
-- 1. SALES SUMMARY
-- ============================================================

CREATE OR REPLACE VIEW vw_sales_summary AS
SELECT
    COUNT(*) AS sales_rows,
    COUNT(DISTINCT order_id) AS total_orders,
    COUNT(DISTINCT customer_key) AS total_customers,
    SUM(sales) AS total_revenue,
    SUM(profit) AS total_profit,
    SUM(quantity) AS total_units,
    AVG(discount) AS average_discount,
    CASE
        WHEN SUM(sales) = 0 THEN 0
        ELSE SUM(profit) / SUM(sales)
    END AS profit_margin
FROM fact_sales;


-- ============================================================
-- 2. PRODUCT PERFORMANCE
-- ============================================================

CREATE OR REPLACE VIEW vw_product_performance AS
SELECT
    p.product_key,
    p.product_id,
    p.product_name,
    p.category,
    p.sub_category,

    COUNT(f.order_id) AS order_lines,
    COUNT(DISTINCT f.order_id) AS orders,

    SUM(f.quantity) AS units_sold,
    SUM(f.sales) AS revenue,
    SUM(f.profit) AS profit,

    AVG(f.discount) AS average_discount,

    CASE
        WHEN SUM(f.sales) = 0 THEN 0
        ELSE SUM(f.profit) / SUM(f.sales)
    END AS profit_margin

FROM fact_sales f
JOIN dim_product p
    ON f.product_key = p.product_key

GROUP BY
    p.product_key,
    p.product_id,
    p.product_name,
    p.category,
    p.sub_category;


-- ============================================================
-- 3. REGION PERFORMANCE
-- ============================================================

CREATE OR REPLACE VIEW vw_region_performance AS
SELECT
    r.region_key,
    r.region,
    r.state,
    r.city,

    COUNT(f.order_id) AS order_lines,
    COUNT(DISTINCT f.order_id) AS orders,

    SUM(f.quantity) AS units_sold,
    SUM(f.sales) AS revenue,
    SUM(f.profit) AS profit,

    AVG(f.discount) AS average_discount,

    CASE
        WHEN SUM(f.sales) = 0 THEN 0
        ELSE SUM(f.profit) / SUM(f.sales)
    END AS profit_margin

FROM fact_sales f
JOIN dim_region r
    ON f.region_key = r.region_key

GROUP BY
    r.region_key,
    r.region,
    r.state,
    r.city;


-- ============================================================
-- 4. CUSTOMER PERFORMANCE
-- ============================================================

CREATE OR REPLACE VIEW vw_customer_performance AS
SELECT
    c.customer_key,
    c.customer_id,
    c.customer_name,
    c.segment,

    COUNT(DISTINCT f.order_id) AS orders,

    SUM(f.quantity) AS units_purchased,
    SUM(f.sales) AS revenue,
    SUM(f.profit) AS profit,

    AVG(f.discount) AS average_discount,

    CASE
        WHEN SUM(f.sales) = 0 THEN 0
        ELSE SUM(f.profit) / SUM(f.sales)
    END AS profit_margin

FROM fact_sales f
JOIN dim_customer c
    ON f.customer_key = c.customer_key

GROUP BY
    c.customer_key,
    c.customer_id,
    c.customer_name,
    c.segment;


-- ============================================================
-- 5. CATEGORY PERFORMANCE
-- ============================================================

CREATE OR REPLACE VIEW vw_category_performance AS
SELECT
    p.category,

    COUNT(DISTINCT f.order_id) AS orders,
    SUM(f.quantity) AS units_sold,
    SUM(f.sales) AS revenue,
    SUM(f.profit) AS profit,

    AVG(f.discount) AS average_discount,

    CASE
        WHEN SUM(f.sales) = 0 THEN 0
        ELSE SUM(f.profit) / SUM(f.sales)
    END AS profit_margin

FROM fact_sales f
JOIN dim_product p
    ON f.product_key = p.product_key

GROUP BY
    p.category;


-- ============================================================
-- 6. SEGMENT PERFORMANCE
-- ============================================================

CREATE OR REPLACE VIEW vw_segment_performance AS
SELECT
    c.segment,

    COUNT(DISTINCT f.order_id) AS orders,
    COUNT(DISTINCT f.customer_key) AS customers,

    SUM(f.quantity) AS units_sold,
    SUM(f.sales) AS revenue,
    SUM(f.profit) AS profit,

    AVG(f.discount) AS average_discount,

    CASE
        WHEN SUM(f.sales) = 0 THEN 0
        ELSE SUM(f.profit) / SUM(f.sales)
    END AS profit_margin

FROM fact_sales f
JOIN dim_customer c
    ON f.customer_key = c.customer_key

GROUP BY
    c.segment;


-- ============================================================
-- 7. MONTHLY PERFORMANCE
-- ============================================================

CREATE OR REPLACE VIEW vw_monthly_performance AS
SELECT
    d.year,
    d.month,
    d.quarter,

    COUNT(DISTINCT f.order_id) AS orders,
    COUNT(DISTINCT f.customer_key) AS customers,

    SUM(f.quantity) AS units_sold,
    SUM(f.sales) AS revenue,
    SUM(f.profit) AS profit,

    AVG(f.discount) AS average_discount,

    CASE
        WHEN SUM(f.sales) = 0 THEN 0
        ELSE SUM(f.profit) / SUM(f.sales)
    END AS profit_margin

FROM fact_sales f
JOIN dim_date d
    ON f.date_key = d.date_key

GROUP BY
    d.year,
    d.month,
    d.quarter;