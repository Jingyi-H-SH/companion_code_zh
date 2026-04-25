# 《人工智能与健康传播：基础与应用》配套代码

这个仓库是《人工智能与健康传播：基础与应用》的配套代码仓库。它包含 5 套适合初学者上手的演示代码，用来把书中的教学内容进一步落实为可运行、可观察、可修改的示例。每一章都至少包含一个真实的 OpenAI API 调用，并且会把运行进度可视化到 `outputs/progress_dashboard.png`。

## 这个仓库和本书是什么关系

- 这不是一套独立于本书之外的零散代码，而是围绕本书教学内容整理出来的配套代码。
- 每个章节文件夹都对应书中的一个实践主题，用来帮助读者把概念理解延伸到实际操作。
- 中文仓库面向中文教学、中文课堂演示和中文读者阅读体验。
- 英文仓库保留相同逻辑，但更适合国际读者、GitHub 展示和英文课堂协作。

## 这个仓库适合谁

- 想做课堂演示的教师。
- 第一次接触 OpenAI API 的学生。
- 更喜欢按步骤理解流程、而不是直接看黑箱结果的读者。

## 快速开始

1. 先创建并激活虚拟环境。
2. 运行 `pip install -r requirements.txt` 安装依赖。
3. 进入任意章节后执行 `python run_demo.py`。如果没有提前设置 `OPENAI_API_KEY`，脚本会安全地提示你输入。
4. 如果你想换模型，可以设置 `OPENAI_MODEL`；本仓库默认值是 `gpt-4.1-mini`。

### 推荐的终端命令

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd chapter02_message_mining
python run_demo.py
```

## API Key 在这里怎么用

- 如果你的终端环境里已经有 `OPENAI_API_KEY`，代码会直接使用。
- 如果没有，`run_demo.py` 会在运行时提示你输入一次，并通过环境变量传给后续脚本。
- API key 不会被写入仓库文件。
- 如果你想换模型，可以设置 `OPENAI_MODEL`；默认值是 `gpt-4.1-mini`。

## 章节说明

- `chapter02_message_mining`: **居民健康留言挖掘**. 对短健康留言进行分类，并生成适合读者查看的回应建议。
- `chapter03_water_habit_helper`: **饮水习惯助手**. 估计用户未完成饮水目标的风险，并生成个性化提醒。
- `chapter04_health_agent_lab`: **健康沟通 Agent 实验室**. 模拟简短的健康支持对话，并审查共情、安全和表达清晰度。
- `chapter05_bias_audit`: **偏差审计**. 为不同用户画像生成健康回答，并比较群体之间的差异。
- `chapter06_ai_compliance_checker`: **AI 合规检查器**. 围绕隐私、可解释性和公平性检查一个示例健康 AI 系统。

## 运行一章后会发生什么

- 每一章都会把中间结果写入 `outputs/`，便于逐步查看。
- 每完成一步都会更新一次进度 JSON。
- 最后会自动生成可视化进度图 `outputs/progress_dashboard.png`。
- API key 不会写入磁盘，只会从环境变量读取或在运行时临时输入。

## 目录结构怎么理解

- `run_demo.py`：该章的总入口。
- `src/`：真正执行任务的分步脚本。
- `data/`：用于演示的小样本输入数据。
- `outputs/`：生成的表格、报告、图表和进度文件。
- `app/progress_dashboard.py`：把进度 JSON 转成可视化 PNG。
- `notebooks/`：适合读者边看边跑的讲解版 Notebook。

## 推荐的使用方式

1. 先阅读本书中对应的内容或案例。
2. 打开这个仓库里相应的章节文件夹。
3. 运行 `python run_demo.py`，然后查看 `outputs/` 里的结果。
4. 如果希望更慢、更细地理解流程，再打开 `notebooks/` 里的讲解版 Notebook。

## 常见问题

- 如果报错 `No module named openai`，请重新执行 `pip install -r requirements.txt`。
- 如果模型调用失败，请先确认 API key 是否有效，以及你的账号是否可以访问 `OPENAI_MODEL` 指定的模型。
- 第 3 章即使没有安装 `streamlit`，也可以用命令行预览模式查看结果。
- 如果运行中断，请先去看 `outputs/` 里最后生成的文件。这套代码特意保留了中间结果，方便排查。
