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
        "title": "第 5 章运行进度",
        "subtitle": "针对不同用户画像生成健康回答，并检查潜在群体差异。",
        "steps": steps,
        "metrics": metrics or [],
        "notes": notes or [
            "每一个提示词和用户画像组合都会单独调用一次 LLM。",
            "随后会用结构化审查步骤对共情、可操作性、可及性和安全性评分。",
            "报告会自动标记不同群体之间差异过大的地方。",
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
    run_script("src/run_batch_eval.py", steps, "生成回答并完成结构化质量评分", env)
    run_script("src/compare_groups.py", steps, "按群体汇总分数", env)
    run_script("src/score_bias_flags.py", steps, "标记差异较大的指标", env)
    run_script("src/render_bias_report.py", steps, "生成面向读者的 Markdown 报告", env)
    batch = pd.read_csv(OUTPUTS / "batch_eval.csv")
    flags = pd.read_csv(OUTPUTS / "bias_flags.csv")
    metrics = [
        {"label": "回答数", "value": str(len(batch))},
        {"label": "提示词", "value": str(batch['prompt_id'].nunique())},
        {"label": "画像数", "value": str(batch['profile_id'].nunique())},
        {"label": "标记数", "value": str(len(flags))},
    ]
    write_progress(steps, metrics=metrics)
    subprocess.run([sys.executable, str(ROOT / "app" / "progress_dashboard.py")], cwd=ROOT, env=env, check=True)
    print("第 5 章演示运行完成。")


if __name__ == "__main__":
    main()
