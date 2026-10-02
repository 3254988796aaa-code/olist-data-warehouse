import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

schema = """
数据仓库表结构（Hive）：

1. dwd_order_fact（订单事实表，粒度=订单行）
   字段：order_id, order_item_id, customer_key, product_key, 
        seller_key, date_key, order_status, price, freight_value, payment_value
   注意：payment_value 是订单级支付金额，多行订单会重复，计算 GMV 必须用 price

2. dwd_dim_customer（客户维度）
   字段：customer_key, customer_unique_id, customer_zip_code_prefix, 
        customer_city, customer_state

3. dwd_dim_product（商品维度）
   字段：product_key, product_category_name, product_category_name_english, 
        product_weight_g, product_length_cm, product_height_cm, product_width_cm

4. dwd_dim_seller（商家维度）
   字段：seller_key, seller_zip_code_prefix, seller_city, seller_state

5. dwd_dim_date（时间维度）
   字段：date_key（YYYYMMDD）, date_str, year, month, day, quarter, week, weekday
"""

# 业务规则：必须显式告诉 AI
rules = """
业务规则（必须遵守）：
1. GMV = SUM(price)，不要用 payment_value
2. 计算销售额/订单数时，必须排除取消和无效订单：
   WHERE order_status NOT IN ('canceled', 'unavailable')
3. 品类名称输出用 product_category_name_english
4. 表名不加数据库前缀
5. 只返回 SQL，不要 markdown 代码块，不要解释
"""

# Few-shot 示例
examples = """
示例1：
问题：2017年11月24日当天的总GMV是多少？
SQL：SELECT SUM(price) AS total_gmv FROM dwd_order_fact WHERE date_key = '20171124' AND order_status NOT IN ('canceled','unavailable')

示例2：
问题：销售额最高的前5个商品品类是什么？
SQL：SELECT p.product_category_name_english AS category, SUM(f.price) AS sales FROM dwd_order_fact f JOIN dwd_dim_product p ON f.product_key = p.product_key WHERE f.order_status NOT IN ('canceled','unavailable') GROUP BY p.product_category_name_english ORDER BY sales DESC LIMIT 5
"""

questions = [
    "2017年11月24日当天的总GMV是多少？",
    "销售额最高的前5个商品品类是什么？",
    "圣保罗州（SP）的客户总共下了多少单？",
]

for q in questions:
    prompt = f"""你是一个 Hive SQL 专家。根据表结构、业务规则和示例，把用户问题转成 Hive SQL。

{schema}

{rules}

{examples}

用户问题：{q}

只返回 SQL："""

    response = client.chat.completions.create(
        model="qwen3.8-flash",
        messages=[{"role": "user", "content": prompt}]
    )

    sql = response.choices[0].message.content.strip()
    print(f"\n{'=' * 60}")
    print(f"问题：{q}")
    print(f"{'=' * 60}")
    print(sql)