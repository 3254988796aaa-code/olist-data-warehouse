from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_timestamp

spark = SparkSession.builder \
    .appName("Olist ETL") \
    .config("hive.metastore.uris", "thrift://hive-metastore:9083") \
    .enableHiveSupport() \
    .getOrCreate()

spark.sql("DROP TABLE IF EXISTS olist_orders_clean")

orders_df = spark.read.csv("hdfs://namenode:8020/olist/raw/olist_orders_dataset.csv", header=True, inferSchema=True)

time_cols = [
    'order_purchase_timestamp', 'order_approved_at',
    'order_delivered_carrier_date', 'order_delivered_customer_date',
    'order_estimated_delivery_date'
]
for c in time_cols:
    orders_df = orders_df.withColumn(c, to_timestamp(col(c), "yyyy-MM-dd HH:mm:ss"))

orders_clean = orders_df.na.drop(subset=["order_id", "customer_id", "order_status"])
orders_clean.write.mode("overwrite").saveAsTable("olist_orders_clean")

print("ETL completed")
spark.stop()
