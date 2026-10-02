-- ADS 层建表 DDL

CREATE TABLE IF NOT EXISTS ads_sales_overview (
    total_gmv DOUBLE COMMENT '总GMV',
    total_orders BIGINT COMMENT '总订单数',
    total_customers BIGINT COMMENT '总客户数',
    total_items BIGINT COMMENT '总商品件数',
    avg_order_value DOUBLE COMMENT '平均客单价',
    avg_freight DOUBLE COMMENT '平均运费',
    cancel_rate DOUBLE COMMENT '取消率'
)
STORED AS PARQUET
TBLPROPERTIES ('parquet.compression'='SNAPPY');

CREATE TABLE IF NOT EXISTS ads_monthly_trend (
    year INT COMMENT '年',
    month INT COMMENT '月',
    ym STRING COMMENT '年月(YYYY-MM)',
    order_cnt BIGINT COMMENT '订单数',
    gmv DOUBLE COMMENT 'GMV',
    customer_cnt BIGINT COMMENT '客户数'
)
STORED AS PARQUET
TBLPROPERTIES ('parquet.compression'='SNAPPY');

CREATE TABLE IF NOT EXISTS ads_category_rank (
    rank_no INT COMMENT '排名',
    product_category STRING COMMENT '品类',
    order_cnt BIGINT COMMENT '订单数',
    item_cnt BIGINT COMMENT '商品件数',
    sales_amount DOUBLE COMMENT '销售额',
    avg_price DOUBLE COMMENT '平均单价'
)
STORED AS PARQUET
TBLPROPERTIES ('parquet.compression'='SNAPPY');

CREATE TABLE IF NOT EXISTS ads_region_sales (
    customer_state STRING COMMENT '州代码',
    state_name STRING COMMENT '州全称',
    order_cnt BIGINT COMMENT '订单数',
    customer_cnt BIGINT COMMENT '客户数',
    sales_amount DOUBLE COMMENT '销售额',
    avg_order_value DOUBLE COMMENT '客单价'
)
STORED AS PARQUET
TBLPROPERTIES ('parquet.compression'='SNAPPY');

CREATE TABLE IF NOT EXISTS ads_rfm_summary (
    rfm_level STRING COMMENT 'RFM层级',
    user_cnt BIGINT COMMENT '用户数',
    user_pct DOUBLE COMMENT '用户占比(%)',
    total_monetary DOUBLE COMMENT '总消费',
    avg_monetary DOUBLE COMMENT '人均消费'
)
STORED AS PARQUET
TBLPROPERTIES ('parquet.compression'='SNAPPY');