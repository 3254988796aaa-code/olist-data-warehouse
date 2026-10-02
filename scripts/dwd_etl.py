from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_date, date_format, year, month, dayofmonth, quarter, weekofyear, dayofweek, sum as _sum, coalesce, lit

spark = SparkSession.builder \
    .appName("Olist DWD ETL") \
    .config("hive.metastore.uris", "thrift://hive-metastore:9083") \
    .enableHiveSupport() \
    .getOrCreate()

# ============ 1. 客户维度 ============
print(">>> 构建 dwd_dim_customer")
df_customer = spark.sql("""
    SELECT
        customer_id AS customer_key,
        customer_unique_id,
        customer_zip_code_prefix,
        customer_city,
        customer_state
    FROM ods_olist_customers
""")
df_customer.write.mode("overwrite").saveAsTable("dwd_dim_customer")
print(f"dwd_dim_customer: {df_customer.count()} 行")

# ============ 2. 商品维度 ============
print(">>> 构建 dwd_dim_product")
df_product = spark.sql("""
    SELECT
        p.product_id AS product_key,
        p.product_category_name,
        coalesce(t.product_category_name_english, p.product_category_name, 'unknown') AS product_category_name_english,
        p.product_weight_g,
        p.product_length_cm,
        p.product_height_cm,
        p.product_width_cm
    FROM ods_olist_products p
    LEFT JOIN ods_product_category_name_translation t
        ON p.product_category_name = t.product_category_name
""")
df_product.write.mode("overwrite").saveAsTable("dwd_dim_product")
print(f"dwd_dim_product: {df_product.count()} 行")

# ============ 3. 商家维度 ============
print(">>> 构建 dwd_dim_seller")
df_seller = spark.sql("""
    SELECT
        seller_id AS seller_key,
        seller_zip_code_prefix,
        seller_city,
        seller_state
    FROM ods_olist_sellers
""")
df_seller.write.mode("overwrite").saveAsTable("dwd_dim_seller")
print(f"dwd_dim_seller: {df_seller.count()} 行")

# ============ 4. 时间维度 ============
print(">>> 构建 dwd_dim_date")
df_date = spark.sql("""
    SELECT DISTINCT
        date_format(order_purchase_timestamp, 'yyyyMMdd') AS date_key,
        date_format(order_purchase_timestamp, 'yyyy-MM-dd') AS date_str,
        year(order_purchase_timestamp) AS year,
        month(order_purchase_timestamp) AS month,
        dayofmonth(order_purchase_timestamp) AS day,
        quarter(order_purchase_timestamp) AS quarter,
        weekofyear(order_purchase_timestamp) AS week,
        dayofweek(order_purchase_timestamp) AS weekday
    FROM ods_olist_orders
    WHERE order_purchase_timestamp IS NOT NULL
""")
df_date.write.mode("overwrite").saveAsTable("dwd_dim_date")
print(f"dwd_dim_date: {df_date.count()} 行")

# ============ 5. 订单事实表 ============
print(">>> 构建 dwd_order_fact")
df_fact = spark.sql("""
    SELECT
        oi.order_id,
        oi.order_item_id,
        o.customer_id AS customer_key,
        oi.product_id AS product_key,
        oi.seller_id AS seller_key,
        date_format(o.order_purchase_timestamp, 'yyyyMMdd') AS date_key,
        o.order_status,
        oi.price,
        oi.freight_value,
        pay.payment_value
    FROM ods_olist_order_items oi
    INNER JOIN ods_olist_orders o
        ON oi.order_id = o.order_id
    LEFT JOIN (
        SELECT order_id, sum(payment_value) AS payment_value
        FROM ods_olist_order_payments
        GROUP BY order_id
    ) pay
        ON oi.order_id = pay.order_id
    WHERE o.order_status IS NOT NULL
""")
df_fact.write.mode("overwrite").saveAsTable("dwd_order_fact")
print(f"dwd_order_fact: {df_fact.count()} 行")

print("DWD ETL completed")
spark.stop()