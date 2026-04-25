# 健康沟通 Agent 实验室

这一章是整个仓库里最明确的定制 chatbot 示例。它把系统策略、多轮记忆、安全规则、检索模块和 LLM 回复生成组合到一起。

## 工作流程

1. 加载一个简短对话场景和助手策略。
2. 跟踪用户状态，并检查是否触发显式升级规则。
3. 从本地知识库中检索最相关的健康支持片段。
4. 结合策略、多轮记忆和检索上下文生成助手回复。
5. 最后用 LLM 量表审查整段对话。

## 核心技术概念

- 定制化 chatbot 架构
- 系统提示词 + 多轮对话记忆
- 生成前的安全守卫逻辑
- 把 RAG 嵌入对话工作流
- 使用 LLM-as-judge 做质量审查

## 如何运行

1. 在终端中进入当前章节文件夹。
2. 运行 `python run_demo.py`。
3. 如果环境里还没有 `OPENAI_API_KEY`，脚本会提示你输入。
4. 运行结束后，查看 `outputs/`。

## 建议重点查看的文件

- `app/conversation_playground.py`
- `src/generate_agent_reply.py`
- `data/health_knowledge_base.json`
- `outputs/conversation_transcripts.csv`
