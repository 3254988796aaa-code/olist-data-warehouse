# Olist Data Warehouse

鍩轰簬 Hadoop + Hive + Spark 鐨勫畬鏁存暟浠撻」鐩紝閲囩敤 ODS -> DWD -> DWS -> ADS 鍥涘眰鏋舵瀯銆?
## 鎶€鏈爤

| 缁勪欢 | 鐗堟湰 | 鐢ㄩ€?|
|---|---|---|
| Hadoop | 3.3.6 | HDFS + YARN |
| Hive | 4.0.0 | 鏁版嵁浠撳簱 + Metastore |
| Spark | 3.5.1 | PySpark ETL |
| PostgreSQL | 16 | Hive Metastore 鍚庣 |
| Tableau Public | 2025.3 | 鏁版嵁鍙鍖?|

## 鏁版嵁婧?
Kaggle Olist 宸磋タ鐢靛晢鏁版嵁闆嗭紝9 寮?CSV锛岀害 10 涓囪鍗曘€?
## 鏁颁粨鍒嗗眰

| 灞傛 | 琛ㄦ暟 | 璇存槑 |
|---|---|---|
| ODS | 9 | 鍘熷鏁版嵁鎺ュ叆锛屼笉鍋氭竻娲?|
| DWD | 5 | 鏄熷瀷妯″瀷锛? 缁磋〃 + 1 璁㈠崟浜嬪疄琛?|
| DWS | 5 | 鏃?GMV / 鍝佺被 / 鍦板尯 / RFM / 鍛ㄦ眹鎬?|
| ADS | 5 | 搴旂敤灞傛寚鏍囷細鎬昏 / 鏈堝害瓒嬪娍 / 鍝佺被鎺掕 / 鍦板尯鎺掕 / RFM 鍒嗗眰 |

## 鍙鍖栫湅鏉匡紙Tableau Public锛?
5 寮犳牳蹇冨浘琛細鏈堝害 GMV 瓒嬪娍銆佸搧绫婚攢鍞帓琛屻€佸湴鍖洪攢鍞帓琛屻€丷FM 鐢ㄦ埛鍒嗗眰銆佹牳蹇冩寚鏍囨€昏銆?
## 鏁版嵁娲炲療

- 鎬?GMV锛?3,591,644锛堥浄浜氬皵锛?- 鎬昏鍗曪細98,666
- 瀹㈠崟浠凤細137.75
- 鍙栨秷鐜囷細0.49%
- 榛戜簲鏁堝簲锛?017-11-24 GMV 鏄櫘閫氭棩鐨?3 鍊?- 鍦板尯闆嗕腑搴︼細SP锛堝湥淇濈綏宸烇級鍗犲叏鍥界害 38% 閿€鍞
- 鐑棬鍝佺被锛歨ealth_beauty / watches_gifts / bed_bath_table
- RFM 娲炲療锛氶噸瑕佹尳鐣欏鎴峰崰 23.5%锛屾槸钀ラ攢閲嶇偣鍙洖瀵硅薄

## 鐩綍缁撴瀯
scripts/ # PySpark ETL 鑴氭湰锛堝惈 ads_etl.py锛?sql/ # Hive DDL锛堝惈 ads_ddl.sql锛?docs/ # 椤圭洰鏂囨。
conf/ # 閰嶇疆鏂囦欢
tableau_data/ # Tableau 鏁版嵁 + 宸ヤ綔绨?docker-compose.yml
README.md
## 鐜璇存槑

- 瀛樺偍鏍煎紡锛歅arquet + Snappy
- Warehouse 璺緞锛歨dfs://namenode:8020/user/hive/warehouse
- ETL 涓€寰嬮€氳繃 Spark SQL锛岄伩鍏?Hive on Tez 鏉冮檺闂