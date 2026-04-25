# 《人工智能与健康传播：基础与应用》配套代码

这个仓库是《人工智能与健康传播：基础与应用》的配套代码仓库。它包含 5 套可运行的演示代码，用来把书中的教学内容落实为可以观察、修改、复现的具体工作流。

## 这套配套代码覆盖了哪些基础 LLM 模式？

- **Prompt 设计 + 结构化 JSON 输出**：第 2 章展示怎样让 LLM 返回可直接处理的结构化标签，而不是自由文本。
- **轻量级 RAG（检索增强生成）**：第 2、3、4、6 章都会在调用模型前，先从本地参考资料中检索相关片段。
- **定制化对话 chatbot 设计**：第 4 章把系统提示词、多轮记忆、检索模块和显式安全规则结合在一起。
- **LLM-as-judge 评估模式**：第 5 章把“回答生成”和“回答审查”拆开，便于理解审计逻辑。
- **政策/治理审查工作流**：第 6 章展示如何把清单、检索和结构化评分组合成合规报告。

## 这个仓库和本书是什么关系

- 这个仓库不是零散代码集合，而是本书教学内容的配套实现。
- 每个章节文件夹都对应一个实践主题，用来展示一种或多种核心 LLM 应用模式。
- 中文仓库面向中文教学、中文课堂演示和中文读者。
- 英文仓库保留相同逻辑，但更适合 GitHub 展示、英文课堂和国际协作。

## 快速开始

1. 创建并激活虚拟环境。
2. 运行 `pip install -r requirements.txt`。
3. 进入任意章节文件夹，执行 `python run_demo.py`。
4. 如果环境里没有 `OPENAI_API_KEY`，脚本会安全地提示你输入。

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd chapter04_health_agent_lab
python run_demo.py
```

## 章节地图

- `chapter02_message_mining`：**结构化分类 + 轻量级 RAG**
- `chapter03_water_habit_helper`：**用户状态提示 + 检索式策略生成**
- `chapter04_health_agent_lab`：**定制 chatbot + 多轮记忆 + 安全规则 + RAG**
- `chapter05_bias_audit`：**生成模型 + 审查模型 + 群体比较**
- `chapter06_ai_compliance_checker`：**清单审查 + 治理 RAG + 报告合成**

## 运行之后会得到什么

- 工作流每一步的中间结果都会写入 `outputs/`。
- 每完成一步都会更新一次进度 JSON。
- 每一章都会生成可视化进度图 `outputs/progress_dashboard.png`。
- OpenAI API key 只会从环境变量读取或在运行时临时输入，不会保存到磁盘。
