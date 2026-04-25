# 健康传播与人工智能教学演示代码

这个仓库包含 5 套面向课堂教学的演示代码，依据配套代码文件清单整理而成。

整体设计遵循同一原则：
- 紧贴对应章节的教学目标
- 代码尽量简洁、直观、便于课堂讲解
- 每套案例都可以用一条命令跑通
- 每套案例都内置可视化进度报告机制

## 快速开始

1. 准备 Python 3.10 或更新版本的环境。
2. 安装依赖：

```bash
pip install -r requirements.txt
```

3. 进入任意章节并运行演示：

```bash
cd chapter02_message_mining
python run_demo.py
```

运行后，对应章节的 `outputs/` 文件夹会自动生成结果文件和 `progress_dashboard.png`。

## 仓库结构

- `chapter02_message_mining`
  教学主题：居民健康留言主题分类与情绪标注
- `chapter03_water_habit_helper`
  教学主题：饮水目标预测与个性化提醒生成
- `chapter04_health_agent_lab`
  教学主题：AI 健康沟通机器人的安全性与共情评测
- `chapter05_bias_audit`
  教学主题：健康问答系统的偏见检测
- `chapter06_ai_compliance_checker`
  教学主题：健康咨询 AI 上线前的伦理与治理自查

## 统一约定

- `data/`：存放小型教学数据
- `src/`：存放主要分析或模拟脚本
- `app/`：存放进度看板和轻量演示界面
- `notebooks/`：存放课堂讲解用 notebook
- 每个章节都额外提供一个 `notebooks/*_teaching_demo.ipynb`，适合直接投屏讲解
- `outputs/`：仓库中默认保持为空，运行演示后自动生成

## 上传 GitHub 的建议

```bash
git init
git add .
git commit -m "添加健康传播与人工智能教学演示代码"
```

如果你准备新建远程仓库，建议使用英文仓库名，例如 `health-ai-teaching-demos`，这样后续分享和引用会更方便。
