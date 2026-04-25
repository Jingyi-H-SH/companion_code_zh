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
        "title": "第5章演示进度",
        "subtitle": "健康问答偏见检测台",
        "steps": steps,
        "metrics": metrics or [],
        "notes": notes or [
            "这里故意保留一个并不完美的回答生成器，方便课堂上观察差异是如何出现的。",
            "分组比较方法足够简单，学生可以手动复算并理解判断依据。",
            "偏见提示采用阈值规则，便于解释为什么会触发某个警示。",
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
    run_script("src/run_batch_eval.py", steps, "批量生成回答结果")
    run_script("src/compare_groups.py", steps, "比较不同群体的平均输出")
    run_script("src/score_bias_flags.py", steps, "标记显著差异")
    run_script("src/render_bias_report.py", steps, "生成课堂演示报告")

    flags = pd.read_csv(OUTPUTS / "bias_flags.csv")
    batch = pd.read_csv(OUTPUTS / "batch_eval.csv")
    metrics = [
        {"label": "画像数", "value": str(batch['profile_id'].nunique())},
        {"label": "问题数", "value": str(batch['prompt_id'].nunique())},
        {"label": "警示数", "value": str(len(flags))},
    ]
    write_progress(steps, metrics=metrics)
    subprocess.run([sys.executable, str(ROOT / "app" / "progress_dashboard.py")], cwd=ROOT, check=True)
    print("第5章演示已完成。")


if __name__ == "__main__":
    main()
