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
        "title": "第2章演示进度",
        "subtitle": "居民健康留言主题分类与情绪标注",
        "steps": steps,
        "metrics": metrics or [],
        "notes": notes or [
            "本案例使用透明的关键词规则，方便学生理解每一步为什么这样判断。",
            "整体流程适合单次课堂演示，也适合现场边讲边改代码。",
            "所有输出都会写入 outputs 文件夹，便于课堂展示和课后复盘。",
        ],
    }
    OUTPUTS.mkdir(parents=True, exist_ok=True)
    PROGRESS_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def run_script(script_name, steps, detail):
    subprocess.run([sys.executable, str(ROOT / script_name)], cwd=ROOT, check=True)
    steps.append({"name": detail, "status": "done", "detail": script_name})
    write_progress(steps)


def main():
    steps = []
    write_progress(steps)
    run_script("src/clean_text.py", steps, "清洗留言文本")
    run_script("src/build_features.py", steps, "构建关键词特征")
    run_script("src/train_topic_classifier.py", steps, "预测留言主题")
    run_script("src/rule_sentiment.py", steps, "标注留言情绪")
    run_script("src/plot_results.py", steps, "生成主题与情绪统计图")

    predictions = pd.read_csv(OUTPUTS / "message_predictions.csv")
    metrics = [
        {"label": "留言数", "value": str(len(predictions))},
        {"label": "主题数", "value": str(predictions['predicted_topic'].nunique())},
        {"label": "紧急留言", "value": str((predictions['predicted_sentiment'] == 'urgent').sum())},
    ]
    write_progress(steps, metrics=metrics)
    subprocess.run([sys.executable, str(ROOT / "app" / "progress_dashboard.py")], cwd=ROOT, check=True)
    print("第2章演示已完成。")


if __name__ == "__main__":
    main()
