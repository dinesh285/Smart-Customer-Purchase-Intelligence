-- CUSTOMER PURCHASE PATTERN ANALYSIS USING APACHE PIG
-- Upload a CSV to HDFS before running this script.
-- The uploaded file must contain the 11 columns listed in README.md.
-- Example:
-- hdfs dfs -mkdir -p /user/cloudera/purchase/input
-- hdfs dfs -put -f customer_transactions.csv /user/cloudera/purchase/input/

transactions = LOAD
'/user/cloudera/purchase/input/customer_transactions.csv'
USING PigStorage(',')
AS (
    transaction_id:chararray,
    customer_id:chararray,
    transaction_date:chararray,
    product_id:chararray,
    product_name:chararray,
    category:chararray,
    quantity:int,
    unit_price:double,
    total_amount:double,
    payment_method:chararray,
    city:chararray
);

-- Remove CSV header and invalid rows.
cleaned = FILTER transactions BY
    transaction_id != 'transaction_id'
    AND customer_id IS NOT NULL
    AND total_amount IS NOT NULL;

-- 1. Product-wise sales.
product_groups = GROUP cleaned BY product_name;
product_summary = FOREACH product_groups GENERATE
    group AS product_name,
    SUM(cleaned.quantity) AS units_sold,
    SUM(cleaned.total_amount) AS revenue;
product_ranked = ORDER product_summary BY revenue DESC;
STORE product_ranked INTO
'/user/cloudera/purchase/output/product_summary'
USING PigStorage(',');

-- 2. Customer purchase behaviour.
customer_groups = GROUP cleaned BY customer_id;
customer_summary = FOREACH customer_groups GENERATE
    group AS customer_id,
    COUNT(cleaned) AS total_orders,
    SUM(cleaned.total_amount) AS total_spend,
    AVG(cleaned.total_amount) AS average_order_value;
customer_ranked = ORDER customer_summary BY total_spend DESC;
STORE customer_ranked INTO
'/user/cloudera/purchase/output/customer_summary'
USING PigStorage(',');

-- 3. Category-wise sales.
category_groups = GROUP cleaned BY category;
category_summary = FOREACH category_groups GENERATE
    group AS category,
    SUM(cleaned.quantity) AS units_sold,
    SUM(cleaned.total_amount) AS revenue;
STORE category_summary INTO
'/user/cloudera/purchase/output/category_summary'
USING PigStorage(',');

-- 4. City-wise sales.
city_groups = GROUP cleaned BY city;
city_summary = FOREACH city_groups GENERATE
    group AS city,
    COUNT(cleaned) AS transactions,
    SUM(cleaned.total_amount) AS revenue;
STORE city_summary INTO
'/user/cloudera/purchase/output/city_summary'
USING PigStorage(',');

-- END OF ANALYSIS
