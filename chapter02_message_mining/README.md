# 居民健康留言挖掘

这一章展示一个基础的 LLM 分类工作流：先整理短文本，再检索主题参考资料，然后用结构化 JSON 完成分类，并进一步生成回应建议。

## 工作流程

1. 先整理居民留言文本，并生成简单的特征提示。
2. 再从本地 JSON 参考资料中检索最相关的主题说明片段。
3. 调用 OpenAI API，返回结构化的主题和情绪标签。
4. 根据分类结果生成一条面向公众的简短回应和一条教师备注。
5. 保存输出结果，并生成进度看板。

## 核心技术概念

- 面向分类任务的 Prompt 设计
- 基于 JSON schema 的结构化输出
- 使用本地参考文件实现轻量级 RAG
- 把“分析”和“后续回复生成”拆开处理

## 如何运行

1. 在终端中进入当前章节文件夹。
2. 运行 `python run_demo.py`。
3. 如果环境里还没有 `OPENAI_API_KEY`，脚本会提示你输入。
4. 运行结束后，查看 `outputs/`。

## 建议重点查看的文件

- `src/train_topic_classifier.py`
- `src/rule_sentiment.py`
- `data/topic_reference.json`
- `outputs/message_predictions.csv`
