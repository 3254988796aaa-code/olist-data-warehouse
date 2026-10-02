# AI 取数助手 (Text-to-SQL)

基于通义千问 qwen3.8-flash 的 Text-to-SQL 工具，用自然语言提问，自动生成 Hive SQL。

## 功能

- 自然语言 -> Hive SQL 自动转换
- Prompt 工程：业务规则 + Few-shot 示例
- Streamlit Web 界面

## 验证结果

3 个测试问题生成的 SQL，与 ADS 层官方结果完全一致。

| 问题 | AI 生成 SQL 结果 | 官方结果 |
|---|---|---|
| 2017-11-24 总 GMV | 152,653.74 | 152,653.74 |
| 品类销售 TOP 5 | health_beauty 1,255,695.13 | 一致 |
| SP 州订单数 | 41,125 | 41,125 |

## 核心 Prompt 设计

1. Schema 描述清晰：明确字段含义，特别标注 payment_value 是订单级金额会重复
2. 业务规则显式化：GMV 用 price、排除取消订单、品类用英文名
3. Few-shot 示例：给出 2 个标准问答对

## 使用方法

```bash
pip install -r requirements.txt
set DASHSCOPE_API_KEY=sk-xxxxxxxx
streamlit run app.py
```

浏览器打开 http://localhost:8501

## 文件说明

- app.py：Streamlit Web 界面
- test_llm.py：LLM 连通性测试
- test_text2sql.py：Text-to-SQL 命令行测试
