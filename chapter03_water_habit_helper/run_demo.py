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
        "title": "第3章演示进度",
        "subtitle": "饮水目标预测与个性化提醒助手",
        "steps": steps,
        "metrics": metrics or [],
        "notes": notes or [
            "模型结构刻意保持简单，便于学生直接查看每个特征如何影响风险分数。",
            "提醒建议与预测使用同一组风险特征，便于讲清“预测到干预”的衔接。",
            "即使没有安装 Streamlit，这套演示也能通过命令行正常展示。",
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
    run_script("src/preprocess_habits.py", steps, "预处理饮水记录")
    run_script("src/train_reminder_model.py", steps, "训练简化提醒模型")
    run_script("src/evaluate_model.py", steps, "评估预测效果")
    run_script("src/generate_suggestions.py", steps, "生成个性化提醒建议")

    metrics = json.loads((OUTPUTS / "evaluation.json").read_text(encoding="utf-8"))
    suggestions = pd.read_csv(OUTPUTS / "suggestions.csv")
    metric_cards = [
        {"label": "准确率", "value": f"{metrics['accuracy']:.0%}"},
        {"label": "召回率", "value": f"{metrics['recall']:.0%}"},
        {"label": "建议数", "value": str(len(suggestions))},
    ]
    write_progress(steps, metrics=metric_cards)
    subprocess.run([sys.executable, str(ROOT / "app" / "progress_dashboard.py")], cwd=ROOT, check=True)
    print("第3章演示已完成。")


if __name__ == "__main__":
    main()
