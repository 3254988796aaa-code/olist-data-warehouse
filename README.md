# Olist Data Warehouse

基于 Hadoop + Hive + Spark 的完整数仓项目，采用 ODS -> DWD -> DWS -> ADS 四层架构。

## 技术栈

| 组件 | 版本 | 用途 |
|---|---|---|
| Hadoop | 3.3.6 | HDFS + YARN |
| Hive | 4.0.0 | 数据仓库 + Metastore |
| Spark | 3.5.1 | PySpark ETL |
| PostgreSQL | 16 | Hive Metastore 后端 |
| Tableau Public | 2025.3 | 数据可视化 |

## 数据源

Kaggle Olist 巴西电商数据集，9 张 CSV，约 10 万订单。

## 数仓分层

| 层次 | 表数 | 说明 |
|---|---|---|
| ODS | 9 | 原始数据接入，不做清洗 |
| DWD | 5 | 星型模型：4 维表 + 1 订单事实表 |
| DWS | 5 | 日 GMV / 品类 / 地区 / RFM / 周汇总 |
| ADS | 5 | 应用层指标：总览 / 月度趋势 / 品类排行 / 地区排行 / RFM 分层 |

## 可视化看板（Tableau Public）

5 张核心图表：月度 GMV 趋势、品类销售排行、地区销售排行、RFM 用户分层、核心指标总览。

## 数据洞察

- 总 GMV：13,591,644（雷亚尔）
- 总订单：98,666
- 客单价：137.75
- 取消率：0.49%
- 黑五效应：2017-11-24 GMV 是普通日的 3 倍
- 地区集中度：SP（圣保罗州）占全国约 38% 销售额
- 热门品类：health_beauty / watches_gifts / bed_bath_table
- RFM 洞察：重要挽留客户占 23.5%，是营销重点召回对象

## 目录结构
scripts/ # PySpark ETL 脚本（含 ads_etl.py）
sql/ # Hive DDL（含 ads_ddl.sql）
docs/ # 项目文档
conf/ # 配置文件
tableau_data/ # Tableau 数据 + 工作簿
docker-compose.yml
README.md
## 环境说明

- 存储格式：Parquet + Snappy
- Warehouse 路径：hdfs://namenode:8020/user/hive/warehouse
- ETL 一律通过 Spark SQL，避免 Hive on Tez 权限问题