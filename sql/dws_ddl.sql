-- DWS 层建表 DDL

CREATE TABLE IF NOT EXISTS dws_daily_gmv (
    date_key STRING COMMENT '日期键',
    order_cnt BIGINT COMMENT '订单数',
    item_cnt BIGINT COMMENT '订单项数',
    gmv DOUBLE COMMENT '商品交易总额',
    freight_total DOUBLE COMMENT '运费总额',
    payment_total DOUBLE COMMENT '支付总额',
    avg_order_value DOUBLE COMMENT '客单价'
)
STORED AS PARQUET
TBLPROPERTIES ('parquet.compression'='SNAPPY');

CREATE TABLE IF NOT EXISTS dws_category_sales (
    product_category STRING COMMENT '商品品类',
    order_cnt BIGINT COMMENT '订单数',
    item_cnt BIGINT COMMENT '商品件数',
    sales_amount DOUBLE COMMENT '销售额',
    freight_amount DOUBLE COMMENT '运费'
)
STORED AS PARQUET
TBLPROPERTIES ('parquet.compression'='SNAPPY');

CREATE TABLE IF NOT EXISTS dws_region_sales (
    customer_state STRING COMMENT '客户所在州',
    order_cnt BIGINT COMMENT '订单数',
    customer_cnt BIGINT COMMENT '客户数',
    sales_amount DOUBLE COMMENT '销售额',
    avg_order_value DOUBLE COMMENT '客单价'
)
STORED AS PARQUET
TBLPROPERTIES ('parquet.compression'='SNAPPY');

CREATE TABLE IF NOT EXISTS dws_user_rfm (
    customer_key STRING COMMENT '客户ID',
    recency INT COMMENT '最近一次购买距今天数',
    frequency BIGINT COMMENT '购买频次',
    monetary DOUBLE COMMENT '消费金额',
    r_score INT COMMENT 'R评分',
    f_score INT COMMENT 'F评分',
    m_score INT COMMENT 'M评分',
    rfm_segment STRING COMMENT 'RFM分层'
)
STORED AS PARQUET
TBLPROPERTIES ('parquet.compression'='SNAPPY');

CREATE TABLE IF NOT EXISTS dws_weekly_summary (
    year INT COMMENT '年',
    week INT COMMENT '周次',
    order_cnt BIGINT COMMENT '订单数',
    gmv DOUBLE COMMENT '商品交易总额',
    active_customers BIGINT COMMENT '活跃客户数'
)
STORED AS PARQUET
TBLPROPERTIES ('parquet.compression'='SNAPPY');