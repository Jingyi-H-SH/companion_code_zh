# 居民健康留言挖掘

对短健康留言进行分类，并生成适合读者查看的回应建议。

## 这套演示适合学什么

- 学习怎样把小样本数据整理成适合 LLM 处理的输入。
- 学习怎样让 OpenAI API 返回结构化 JSON 结果。
- 学习怎样把每一步中间结果都保存下来，方便初学者检查。
- 学习怎样把进度 JSON 变成可视化进度图。

## 如何运行

1. 在终端中进入当前章节文件夹。
2. 运行 `python run_demo.py`。
3. 如果环境里还没有 `OPENAI_API_KEY`，脚本会提示你输入。
4. 运行结束后，查看 `outputs/` 文件夹。

## 主要输出文件

- `outputs/message_predictions.csv`
- `outputs/message_guidance.csv`
- `outputs/progress_dashboard.png`

## 推荐的阅读顺序

1. 先运行 `run_demo.py`。
2. 打开 `outputs/` 里的结果文件。
3. 按照进度图里展示的顺序阅读 `src/` 里的脚本。
4. 如果想要更慢、更细的讲解，再打开 `notebooks/` 中的 Notebook。

## 给初学者的建议

- 先跑通，再读代码，不要一开始就陷在所有脚本细节里。
- 每次运行后都打开生成的 CSV/JSON，看清楚每一步到底做了什么。
- 如果你想换模型，可以设置 `OPENAI_MODEL`。
- 如果你想改造这套演示，最适合先从样本数据入手，再重新运行整条流程。
