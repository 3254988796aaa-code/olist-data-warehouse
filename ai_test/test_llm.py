import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),  # 确保是 sk- 开头的 Key
    # 按量付费的正确地址（北京地域）
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

response = client.chat.completions.create(
    model="qwen3.8-flash",
    messages=[{"role": "user", "content": "用一句话介绍数据仓库"}]
)

print(response.choices[0].message.content)