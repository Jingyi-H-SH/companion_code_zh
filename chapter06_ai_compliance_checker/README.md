# AI 合规检查器

这一章展示一种面向治理场景的 RAG 模式：先检索相关政策参考片段，再根据清单为系统评分，最后把结果合成为报告。

## 工作流程

1. 加载示例系统画像和检查清单。
2. 针对隐私、可解释性和公平性分别检索最相关的治理参考资料。
3. 调用 LLM 进行结构化评分并返回发现项。
4. 把各部分得分汇总成最终合规报告。
5. 输出 JSON、Markdown 和章节得分图。

## 核心技术概念

- 基于清单的 Prompt 设计
- 用于政策/治理审查的 RAG
- 结构化章节评分
- 基于中间审查结果自动合成报告

## 如何运行

1. 在终端中进入当前章节文件夹。
2. 运行 `python run_demo.py`。
3. 如果环境里还没有 `OPENAI_API_KEY`，脚本会提示你输入。
4. 运行结束后，查看 `outputs/`。

## 建议重点查看的文件

- `src/check_privacy.py`
- `src/generate_report.py`
- `data/governance_reference.json`
- `outputs/compliance_report.json`
