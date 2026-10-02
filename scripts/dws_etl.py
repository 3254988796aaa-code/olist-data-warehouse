from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("Olist DWS ETL") \
    .config("hive.metastore.uris", "thrift://hive-metastore:9083") \
    .enableHiveSupport() \
    .getOrCreate()

# 1. 日粒度 GMV
print(">>> 构建 dws_daily_gmv")
spark.sql("""
    INSERT OVERWRITE TABLE dws_daily_gmv
    SELECT
        date_key,
        COUNT(DISTINCT order_id) AS order_cnt,
        COUNT(*) AS item_cnt,
        ROUND(SUM(price), 2) AS gmv,
        ROUND(SUM(freight_value), 2) AS freight_total,
        ROUND(SUM(payment_value), 2) AS payment_total,
        ROUND(SUM(price) / COUNT(DISTINCT order_id), 2) AS avg_order_value
    FROM dwd_order_fact
    WHERE order_status NOT IN ('canceled', 'unavailable')
      AND date_key IS NOT NULL
    GROUP BY date_key
""")

# 2. 品类粒度销售
print(">>> 构建 dws_category_sales")
spark.sql("""
    INSERT OVERWRITE TABLE dws_category_sales
    SELECT
        p.product_category_name_english AS product_category,
        COUNT(DISTINCT f.order_id) AS order_cnt,
        COUNT(*) AS item_cnt,
        ROUND(SUM(f.price), 2) AS sales_amount,
        ROUND(SUM(f.freight_value), 2) AS freight_amount
    FROM dwd_order_fact f
    INNER JOIN dwd_dim_product p ON f.product_key = p.product_key
    WHERE f.order_status NOT IN ('canceled', 'unavailable')
    GROUP BY p.product_category_name_english
""")

# 3. 地区粒度销售
print(">>> 构建 dws_region_sales")
spark.sql("""
    INSERT OVERWRITE TABLE dws_region_sales
    SELECT
        c.customer_state,
        COUNT(DISTINCT f.order_id) AS order_cnt,
        COUNT(DISTINCT f.customer_key) AS customer_cnt,
        ROUND(SUM(f.price), 2) AS sales_amount,
        ROUND(SUM(f.price) / COUNT(DISTINCT f.order_id), 2) AS avg_order_value
    FROM dwd_order_fact f
    INNER JOIN dwd_dim_customer c ON f.customer_key = c.customer_key
    WHERE f.order_status NOT IN ('canceled', 'unavailable')
    GROUP BY c.customer_state
""")

# 4. 用户 RFM
print(">>> 构建 dws_user_rfm")
spark.sql("""
    INSERT OVERWRITE TABLE dws_user_rfm
    WITH rfm_base AS (
        SELECT
            f.customer_key,
            DATEDIFF('2018-10-01', MAX(d.date_str)) AS recency,
            COUNT(DISTINCT f.order_id) AS frequency,
            ROUND(SUM(f.price), 2) AS monetary
        FROM dwd_order_fact f
        LEFT JOIN dwd_dim_date d ON f.date_key = d.date_key
        WHERE f.order_status NOT IN ('canceled', 'unavailable')
        GROUP BY f.customer_key
    ),
    rfm_score AS (
        SELECT
            customer_key, recency, frequency, monetary,
            NTILE(5) OVER (ORDER BY recency DESC) AS r_score,
            NTILE(5) OVER (ORDER BY frequency ASC) AS f_score,
            NTILE(5) OVER (ORDER BY monetary ASC) AS m_score
        FROM rfm_base
    )
    SELECT
        customer_key, recency, frequency, monetary,
        r_score, f_score, m_score,
        CONCAT(CAST(r_score AS STRING), CAST(f_score AS STRING), CAST(m_score AS STRING)) AS rfm_segment
    FROM rfm_score
""")

# 5. 周粒度汇总
print(">>> 构建 dws_weekly_summary")
spark.sql("""
    INSERT OVERWRITE TABLE dws_weekly_summary
    SELECT
        d.year,
        d.week,
        COUNT(DISTINCT f.order_id) AS order_cnt,
        ROUND(SUM(f.price), 2) AS gmv,
        COUNT(DISTINCT f.customer_key) AS active_customers
    FROM dwd_order_fact f
    INNER JOIN dwd_dim_date d ON f.date_key = d.date_key
    WHERE f.order_status NOT IN ('canceled', 'unavailable')
    GROUP BY d.year, d.week
""")

print("DWS ETL completed")
spark.stop()