# Olist Data Warehouse

基于 Hadoop + Hive + Spark 的完整数仓项目，采用 ODS -> DWD -> DWS 分层架构。

## 技术栈
- Hadoop 3.3.6 (HDFS + YARN)
- Hive 4.0.0 (Metastore + HiveServer2)
- Spark 3.5.1 (PySpark ETL)
- PostgreSQL 16 (Metastore 后端)

## 数据源
Kaggle Olist 巴西电商数据集，9 张 CSV，约 10 万订单。

## 数仓分层
| 层次 | 表数 | 说明 |
|---|---|---|
| ODS | 9 | 原始数据接入 |
| DWD | 5 | 星型模型：4 维表 + 1 事实表 |
| DWS | 5 | 日 GMV / 品类 / 地区 / RFM / 周汇总 |

## 项目亮点
- ODS -> DWD -> DWS 全链路 Spark ETL
- DWD 星型模型：客户 / 商品 / 商家 / 时间 4 张维表 + 订单事实表
- 商品维度 LEFT JOIN 品类翻译表（葡语转英语）
- RFM 用户分层
- 数据验证：
  - 2017-11-24 黑五 GMV 是普通日的 3 倍
  - SP 州占全巴西约 50% 销售额
  - 热门品类：health_beauty / watches_gifts / bed_bath_table

## 目录结构scripts/ # PySpark ETL 脚本
sql/ # Hive DDL
docs/ # 项目文档
conf/ # 配置文件
docker-compose.yml
README.md
## 环境说明
- 存储格式：Parquet + Snappy
- Warehouse 路径：hdfs://namenode:8020/user/hive/warehouse