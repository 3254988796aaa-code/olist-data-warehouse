# ODS 层数据接入规范

## 一、数据源
- 来源：Olist 巴西电商数据集（Kaggle）
- 原始文件：9 张 CSV，存放在 HDFS `/olist/raw/`
- 原始文件总大小约 143 MB

## 二、表命名规范
- 格式：`ods_<源表名>`
- 示例：`olist_orders_dataset.csv` → `ods_olist_orders`
- 例外：`product_category_name_translation.csv` → `ods_product_category_name_translation`

## 三、存储规范
- 文件格式：Parquet（列式存储，压缩比高）
- 压缩算法：Snappy
- 表类型：Managed Table（内部表）
- 存储位置：`hdfs://namenode:8020/user/hive/warehouse/`

## 四、字段处理规范
- 时间字段统一转为 `timestamp` 类型
- 涉及字段：
  - `olist_orders_dataset`：order_purchase_timestamp、order_approved_at、order_delivered_carrier_date、order_delivered_customer_date、order_estimated_delivery_date
  - `olist_order_items_dataset`：shipping_limit_date
  - `olist_order_reviews_dataset`：review_creation_date、review_answer_timestamp
- 其余字段保持原始类型（inferSchema 自动推断）
- ODS 层不做清洗、不去重、不补全空值（保持原始状态）

## 五、入库方式
- 引擎：Spark 3.5.1
- 方式：DataFrame `write.mode("overwrite").saveAsTable()`
- 每次全量覆盖，便于重跑

## 六、行数校验基线

| 表名 | 源 CSV 行数 | ODS 表行数 | 一致性 |
|---|---|---|---|
| ods_olist_customers | 99,441 | 99,441 | ✅ |
| ods_olist_geolocation | 1,000,163 | 1,000,163 | ✅ |
| ods_olist_order_items | 112,650 | 112,650 | ✅ |
| ods_olist_order_payments | 103,886 | 103,886 | ✅ |
| ods_olist_order_reviews | 99,224 | 104,162 | ⚠️ 评论表存在同订单多评 |
| ods_olist_orders | 99,441 | 99,441 | ✅ |
| ods_olist_products | 32,951 | 32,951 | ✅ |
| ods_olist_sellers | 3,095 | 3,095 | ✅ |
| ods_product_category_name_translation | 71 | 71 | ✅ |

## 七、数据质量问题（留给 DWD 层处理）
1. **订单表**：order_approved_at 空值率 0.16%，order_delivered_customer_date 空值率 2.98%（未完成订单）
2. **评论表**：存在重复评论，DWD 层需按 order_id 去重
3. **商品表**：product_category_name 存在空值
4. **地理位置表**：同一邮编存在多个经纬度，需要聚合

## 八、更新记录
- 2026-10-01：首次全量入库，9 表全部成功
