from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("Olist ADS ETL") \
    .config("hive.metastore.uris", "thrift://hive-metastore:9083") \
    .enableHiveSupport() \
    .getOrCreate()

# 1. 总览指标
print(">>> 构建 ads_sales_overview")
spark.sql("""
    INSERT OVERWRITE TABLE ads_sales_overview
    SELECT
        ROUND(SUM(price), 2) AS total_gmv,
        COUNT(DISTINCT order_id) AS total_orders,
        COUNT(DISTINCT customer_key) AS total_customers,
        COUNT(*) AS total_items,
        ROUND(SUM(price) / COUNT(DISTINCT order_id), 2) AS avg_order_value,
        ROUND(SUM(freight_value) / COUNT(DISTINCT order_id), 2) AS avg_freight,
        ROUND(
            SUM(CASE WHEN order_status IN ('canceled','unavailable') THEN 1 ELSE 0 END)
            / COUNT(*) * 100, 2
        ) AS cancel_rate
    FROM dwd_order_fact
""")

# 2. 月度趋势
print(">>> 构建 ads_monthly_trend")
spark.sql("""
    INSERT OVERWRITE TABLE ads_monthly_trend
    SELECT
        d.year,
        d.month,
        CONCAT(CAST(d.year AS STRING), '-', LPAD(CAST(d.month AS STRING), 2, '0')) AS ym,
        COUNT(DISTINCT f.order_id) AS order_cnt,
        ROUND(SUM(f.price), 2) AS gmv,
        COUNT(DISTINCT f.customer_key) AS customer_cnt
    FROM dwd_order_fact f
    INNER JOIN dwd_dim_date d ON f.date_key = d.date_key
    WHERE f.order_status NOT IN ('canceled','unavailable')
    GROUP BY d.year, d.month
    ORDER BY d.year, d.month
""")

# 3. 品类排行（取 TOP 20）
print(">>> 构建 ads_category_rank")
spark.sql("""
    INSERT OVERWRITE TABLE ads_category_rank
    SELECT
        ROW_NUMBER() OVER (ORDER BY sales_amount DESC) AS rank_no,
        product_category,
        order_cnt,
        item_cnt,
        sales_amount,
        ROUND(sales_amount / item_cnt, 2) AS avg_price
    FROM (
        SELECT
            product_category,
            order_cnt,
            item_cnt,
            sales_amount
        FROM dws_category_sales
        WHERE product_category IS NOT NULL
          AND product_category != 'unknown'
        ORDER BY sales_amount DESC
        LIMIT 20
    ) t
""")

# 4. 地区销售
print(">>> 构建 ads_region_sales")
spark.sql("""
    INSERT OVERWRITE TABLE ads_region_sales
    SELECT
        customer_state,
        CASE customer_state
            WHEN 'SP' THEN 'São Paulo'
            WHEN 'RJ' THEN 'Rio de Janeiro'
            WHEN 'MG' THEN 'Minas Gerais'
            WHEN 'RS' THEN 'Rio Grande do Sul'
            WHEN 'PR' THEN 'Paraná'
            WHEN 'SC' THEN 'Santa Catarina'
            WHEN 'BA' THEN 'Bahia'
            WHEN 'DF' THEN 'Distrito Federal'
            WHEN 'ES' THEN 'Espírito Santo'
            WHEN 'GO' THEN 'Goiás'
            WHEN 'PE' THEN 'Pernambuco'
            WHEN 'CE' THEN 'Ceará'
            WHEN 'PA' THEN 'Pará'
            WHEN 'MT' THEN 'Mato Grosso'
            WHEN 'MA' THEN 'Maranhão'
            WHEN 'MS' THEN 'Mato Grosso do Sul'
            WHEN 'PB' THEN 'Paraíba'
            WHEN 'PI' THEN 'Piauí'
            WHEN 'RN' THEN 'Rio Grande do Norte'
            WHEN 'AL' THEN 'Alagoas'
            WHEN 'SE' THEN 'Sergipe'
            WHEN 'TO' THEN 'Tocantins'
            WHEN 'RO' THEN 'Rondônia'
            WHEN 'AM' THEN 'Amazonas'
            WHEN 'AC' THEN 'Acre'
            WHEN 'AP' THEN 'Amapá'
            WHEN 'RR' THEN 'Roraima'
            ELSE customer_state
        END AS state_name,
        order_cnt,
        customer_cnt,
        sales_amount,
        avg_order_value
    FROM dws_region_sales
""")

# 5. RFM 分层汇总
print(">>> 构建 ads_rfm_summary")
spark.sql("""
    INSERT OVERWRITE TABLE ads_rfm_summary
    SELECT
        CASE
            WHEN r_score >= 4 AND f_score >= 4 AND m_score >= 4 THEN '重要价值客户'
            WHEN r_score >= 4 AND f_score < 4 AND m_score >= 4 THEN '重要发展客户'
            WHEN r_score < 4 AND f_score >= 4 AND m_score >= 4 THEN '重要保持客户'
            WHEN r_score < 4 AND f_score < 4 AND m_score >= 4 THEN '重要挽留客户'
            WHEN r_score >= 4 AND f_score >= 4 AND m_score < 4 THEN '一般价值客户'
            WHEN r_score >= 4 AND f_score < 4 AND m_score < 4 THEN '一般发展客户'
            WHEN r_score < 4 AND f_score >= 4 AND m_score < 4 THEN '一般保持客户'
            ELSE '一般挽留客户'
        END AS rfm_level,
        COUNT(*) AS user_cnt,
        ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS user_pct,
        ROUND(SUM(monetary), 2) AS total_monetary,
        ROUND(AVG(monetary), 2) AS avg_monetary
    FROM dws_user_rfm
    GROUP BY
        CASE
            WHEN r_score >= 4 AND f_score >= 4 AND m_score >= 4 THEN '重要价值客户'
            WHEN r_score >= 4 AND f_score < 4 AND m_score >= 4 THEN '重要发展客户'
            WHEN r_score < 4 AND f_score >= 4 AND m_score >= 4 THEN '重要保持客户'
            WHEN r_score < 4 AND f_score < 4 AND m_score >= 4 THEN '重要挽留客户'
            WHEN r_score >= 4 AND f_score >= 4 AND m_score < 4 THEN '一般价值客户'
            WHEN r_score >= 4 AND f_score < 4 AND m_score < 4 THEN '一般发展客户'
            WHEN r_score < 4 AND f_score >= 4 AND m_score < 4 THEN '一般保持客户'
            ELSE '一般挽留客户'
        END
    ORDER BY total_monetary DESC
""")

print("ADS ETL completed")
spark.stop()