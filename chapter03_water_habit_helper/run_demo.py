import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parent
OUTPUTS = ROOT / "outputs"
PROGRESS_PATH = OUTPUTS / "progress.json"
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from shared.openai_utils import ensure_openai_credentials


def write_progress(steps, metrics=None, notes=None):
    payload = {
        "title": "第 3 章运行进度",
        "subtitle": "使用 OpenAI API 估计饮水风险，并生成个性化提醒。",
        "steps": steps,
        "metrics": metrics or [],
        "notes": notes or [
            "风险估计只使用当天结束前可获得的信息，避免目标泄漏。",
            "提醒文本会围绕每条记录最可能的阻碍因素来生成。",
            "进度看板会同时展示模型表现和生成建议的数量。",
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
    run_script("src/preprocess_habits.py", steps, "从日志中构建可解释特征", env)
    run_script("src/train_reminder_model.py", steps, "使用 LLM 估计饮水风险", env)
    run_script("src/evaluate_model.py", steps, "评估预测结果并生成图表", env)
    run_script("src/generate_suggestions.py", steps, "生成个性化提醒建议", env)
    metrics = json.loads((OUTPUTS / "evaluation.json").read_text(encoding="utf-8"))
    cards = [
        {"label": "准确率", "value": f"{metrics['accuracy']:.0%}"},
        {"label": "召回率", "value": f"{metrics['recall']:.0%}"},
        {"label": "高风险天数", "value": str(metrics['predicted_miss_days'])},
        {"label": "建议条数", "value": str(metrics['suggestion_rows'])},
    ]
    write_progress(steps, metrics=cards)
    subprocess.run([sys.executable, str(ROOT / "app" / "progress_dashboard.py")], cwd=ROOT, env=env, check=True)
    print("第 3 章演示运行完成。")


if __name__ == "__main__":
    main()
