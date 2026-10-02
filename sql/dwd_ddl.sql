-- ============================================
-- DWD 层建表 DDL
-- ============================================

CREATE TABLE IF NOT EXISTS dwd_dim_customer (
    customer_key STRING COMMENT '客户ID（代理键）',
    customer_unique_id STRING COMMENT '客户唯一标识',
    customer_zip_code_prefix STRING COMMENT '邮编前缀',
    customer_city STRING COMMENT '城市',
    customer_state STRING COMMENT '州'
)
STORED AS PARQUET
TBLPROPERTIES ('parquet.compression'='SNAPPY');

CREATE TABLE IF NOT EXISTS dwd_dim_product (
    product_key STRING COMMENT '商品ID（代理键）',
    product_category_name STRING COMMENT '品类（葡语）',
    product_category_name_english STRING COMMENT '品类（英语）',
    product_weight_g INT COMMENT '重量（克）',
    product_length_cm INT COMMENT '长度（厘米）',
    product_height_cm INT COMMENT '高度（厘米）',
    product_width_cm INT COMMENT '宽度（厘米）'
)
STORED AS PARQUET
TBLPROPERTIES ('parquet.compression'='SNAPPY');

CREATE TABLE IF NOT EXISTS dwd_dim_seller (
    seller_key STRING COMMENT '商家ID（代理键）',
    seller_zip_code_prefix STRING COMMENT '邮编前缀',
    seller_city STRING COMMENT '城市',
    seller_state STRING COMMENT '州'
)
STORED AS PARQUET
TBLPROPERTIES ('parquet.compression'='SNAPPY');

CREATE TABLE IF NOT EXISTS dwd_dim_date (
    date_key STRING COMMENT '日期键（YYYYMMDD）',
    date_str STRING COMMENT '日期字符串',
    year INT COMMENT '年',
    month INT COMMENT '月',
    day INT COMMENT '日',
    quarter INT COMMENT '季度',
    week INT COMMENT '周次',
    weekday INT COMMENT '星期几（1-7）'
)
STORED AS PARQUET
TBLPROPERTIES ('parquet.compression'='SNAPPY');

CREATE TABLE IF NOT EXISTS dwd_order_fact (
    order_id STRING COMMENT '订单ID',
    order_item_id INT COMMENT '订单项序号',
    customer_key STRING COMMENT '客户维度外键',
    product_key STRING COMMENT '商品维度外键',
    seller_key STRING COMMENT '商家维度外键',
    date_key STRING COMMENT '时间维度外键',
    order_status STRING COMMENT '订单状态',
    price DOUBLE COMMENT '商品价格',
    freight_value DOUBLE COMMENT '运费',
    payment_value DOUBLE COMMENT '支付金额'
)
STORED AS PARQUET
TBLPROPERTIES ('parquet.compression'='SNAPPY');