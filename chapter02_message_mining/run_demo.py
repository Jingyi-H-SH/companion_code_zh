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
        "title": "第 2 章运行进度",
        "subtitle": "使用 LLM 对居民健康留言进行主题分类，并生成回应建议。",
        "steps": steps,
        "metrics": metrics or [],
        "notes": notes or [
            "分类器返回的是结构化 JSON，而不是难以复用的自由文本。",
            "每一步中间文件都会保存在 outputs/，便于读者逐步查看。",
            "最后会自动生成进度图，帮助初学者理解整条流程。",
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
    run_script("src/clean_text.py", steps, "整理原始留言文本", env)
    run_script("src/build_features.py", steps, "构建供 LLM 使用的特征提示", env)
    run_script("src/train_topic_classifier.py", steps, "调用 OpenAI API 进行主题和情绪分类", env)
    run_script("src/rule_sentiment.py", steps, "生成面向读者的回复建议", env)
    run_script("src/plot_results.py", steps, "汇总结果并生成图表", env)

    predictions = pd.read_csv(OUTPUTS / "message_predictions.csv")
    metrics = [
        {"label": "留言数", "value": str(len(predictions))},
        {"label": "主题准确率", "value": f"{predictions['topic_match'].mean():.0%}"},
        {"label": "高紧急度", "value": str((predictions['urgency_level'] == 'high').sum())},
        {"label": "平均置信度", "value": f"{predictions['confidence'].mean():.2f}"},
    ]
    write_progress(steps, metrics=metrics)
    subprocess.run([sys.executable, str(ROOT / "app" / "progress_dashboard.py")], cwd=ROOT, env=env, check=True)
    print("第 2 章演示运行完成。")


if __name__ == "__main__":
    main()
