import os
import streamlit as st
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

SCHEMA = """
数据仓库表结构（Hive）：
1. dwd_order_fact（订单事实表，粒度=订单行）
   order_id, order_item_id, customer_key, product_key, seller_key, 
   date_key, order_status, price, freight_value, payment_value
   注意：payment_value 是订单级支付金额，多行订单会重复，GMV 用 price
2. dwd_dim_customer：customer_key, customer_state, customer_city
3. dwd_dim_product：product_key, product_category_name, product_category_name_english
4. dwd_dim_seller：seller_key, seller_state
5. dwd_dim_date：date_key, date_str, year, month, day, quarter, week, weekday
"""

RULES = """
业务规则：
1. GMV = SUM(price)
2. 排除取消和无效订单：WHERE order_status NOT IN ('canceled','unavailable')
3. 品类用 product_category_name_english
4. 表名不加数据库前缀
5. 只返回 SQL，不加 markdown 代码块
"""

st.set_page_config(page_title="Olist AI 取数助手", page_icon="🐳")
st.title("🐳 Olist 电商数仓 AI 取数助手")
st.markdown("用自然语言提问，AI 自动转成 Hive SQL")

question = st.text_input("输入你的问题：", placeholder="例：2017年11月24日的总GMV是多少？")

if st.button("生成 SQL", type="primary"):
    if not question.strip():
        st.warning("请输入问题")
    else:
        prompt = f"""你是 Hive SQL 专家。根据表结构和业务规则，把问题转成 SQL。

{SCHEMA}

{RULES}

用户问题：{question}

只返回 SQL："""

        with st.spinner("AI 正在生成 SQL..."):
            response = client.chat.completions.create(
                model="qwen3.8-flash",
                messages=[{"role": "user", "content": prompt}]
            )
            sql = response.choices[0].message.content.strip()

        st.subheader("生成的 SQL")
        st.code(sql, language="sql")

        st.info("💡 复制上面的 SQL，到 beeline 里执行验证")