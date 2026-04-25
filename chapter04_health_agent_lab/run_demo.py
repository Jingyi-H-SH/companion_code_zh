import json
import subprocess
import sys
from pathlib import Path
import pandas as pd


ROOT = Path(__file__).resolve().parent
OUTPUTS = ROOT / "outputs"
PROGRESS_PATH = OUTPUTS / "progress.json"


def write_progress(steps, metrics=None, notes=None):
    payload = {
        "title": "第4章演示进度",
        "subtitle": "AI健康沟通机器人评测台",
        "steps": steps,
        "metrics": metrics or [],
        "notes": notes or [
            "案例对话刻意保持简短，方便课堂逐轮拆解机器人的回应逻辑。",
            "升级转介规则写得很明确，适合课堂上直接修改并观察效果。",
            "评测重点放在共情、安全性和表达清晰度，而不是只看是否“像人说话”。",
        ],
    }
    OUTPUTS.mkdir(parents=True, exist_ok=True)
    PROGRESS_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def run_script(script_name, steps, label):
    subprocess.run([sys.executable, str(ROOT / script_name)], cwd=ROOT, check=True)
    steps.append({"name": label, "status": "done", "detail": script_name})
    write_progress(steps)


def main():
    steps = []
    write_progress(steps)
    run_script("app/conversation_playground.py", steps, "模拟健康沟通对话")
    run_script("src/review_agent_behavior.py", steps, "评估共情、安全与清晰度")

    transcripts = pd.read_csv(OUTPUTS / "conversation_transcripts.csv")
    reviews = pd.read_csv(OUTPUTS / "review_summary.csv")
    metrics = [
        {"label": "场景数", "value": str(transcripts['scenario_id'].nunique())},
        {"label": "轮次数", "value": str(len(transcripts))},
        {"label": "安全得分", "value": f"{reviews['safety_score'].mean():.0%}"},
    ]
    write_progress(steps, metrics=metrics)
    subprocess.run([sys.executable, str(ROOT / "app" / "progress_dashboard.py")], cwd=ROOT, check=True)
    print("第4章演示已完成。")


if __name__ == "__main__":
    main()
