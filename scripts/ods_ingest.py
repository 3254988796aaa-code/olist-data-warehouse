from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_timestamp

spark = SparkSession.builder \
    .appName("Olist ODS Ingest") \
    .config("hive.metastore.uris", "thrift://hive-metastore:9083") \
    .enableHiveSupport() \
    .getOrCreate()

raw_path = "hdfs://namenode:8020/olist/raw"

file_list = [
    "olist_customers_dataset.csv",
    "olist_geolocation_dataset.csv",
    "olist_order_items_dataset.csv",
    "olist_order_payments_dataset.csv",
    "olist_order_reviews_dataset.csv",
    "olist_orders_dataset.csv",
    "olist_products_dataset.csv",
    "olist_sellers_dataset.csv",
    "product_category_name_translation.csv"
]

time_cols_map = {
    "olist_orders_dataset.csv": [
        'order_purchase_timestamp', 'order_approved_at',
        'order_delivered_carrier_date', 'order_delivered_customer_date',
        'order_estimated_delivery_date'
    ],
    "olist_order_items_dataset.csv": ['shipping_limit_date'],
    "olist_order_reviews_dataset.csv": ['review_creation_date', 'review_answer_timestamp'],
}

for f in file_list:
    table_name = "ods_" + f.replace(".csv", "").replace("_dataset", "")
    path = f"{raw_path}/{f}"
    print(f"Processing {f} -> {table_name}")
    df = spark.read.csv(path, header=True, inferSchema=True)
    if f in time_cols_map:
        for c in time_cols_map[f]:
            if c in df.columns:
                df = df.withColumn(c, to_timestamp(col(c), "yyyy-MM-dd HH:mm:ss"))
    df.write.mode("overwrite").saveAsTable(table_name)
    print(f"Saved {table_name}, count={df.count()}")

print("ODS ingest completed")
spark.stop()
