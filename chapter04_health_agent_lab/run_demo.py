import json
import os
import subprocess
import sys
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parent
OUTPUTS = ROOT / "outputs"
PROGRESS_PATH = OUTPUTS / "progress.json"
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from shared.openai_utils import ensure_openai_credentials


def write_progress(steps, metrics=None, notes=None):
    payload = {
        "title": "第 4 章运行进度",
        "subtitle": "模拟健康支持对话，并用 LLM 审查共情、安全和表达效果。",
        "steps": steps,
        "metrics": metrics or [],
        "notes": notes or [
            "这套流程同时保留了显式的风险升级规则和 LLM 生成回复。",
            "每个场景都会逐轮保存对话记录，便于读者检查。",
            "审查步骤会对共情、安全、清晰度和边界控制进行评分。",
        ],
    }
    OUTPUTS.mkdir(parents=True, exist_ok=True)
    PROGRESS_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def run_script(script_name, steps, label, env):
    subprocess.run([sys.executable, str(ROOT / script_name)], cwd=ROOT, env=env, check=True)
    steps.append({"name": label, "status": "done", "detail": script_name})
    write_progress(steps)


def main():
    env = os.environ.copy()
    env.update(ensure_openai_credentials("zh"))
    env["PYTHONPATH"] = str(REPO_ROOT) + os.pathsep + env.get("PYTHONPATH", "")
    steps = []
    write_progress(steps)
    run_script("app/conversation_playground.py", steps, "生成场景对话记录", env)
    run_script("src/review_agent_behavior.py", steps, "用结构化 LLM 量表审查对话表现", env)
    transcripts = pd.read_csv(OUTPUTS / "conversation_transcripts.csv")
    reviews = pd.read_csv(OUTPUTS / "review_summary.csv")
    metrics = [
        {"label": "场景数", "value": str(transcripts['scenario_id'].nunique())},
        {"label": "轮次数", "value": str(len(transcripts))},
        {"label": "安全得分", "value": f"{reviews['safety_score'].mean():.2f}"},
        {"label": "共情得分", "value": f"{reviews['empathy_score'].mean():.2f}"},
    ]
    write_progress(steps, metrics=metrics)
    subprocess.run([sys.executable, str(ROOT / "app" / "progress_dashboard.py")], cwd=ROOT, env=env, check=True)
    print("第 4 章演示运行完成。")


if __name__ == "__main__":
    main()
