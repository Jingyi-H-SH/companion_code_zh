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
        "title": "第 6 章运行进度",
        "subtitle": "使用基于 LLM 的检查流程审查一个示例健康 AI 系统。",
        "steps": steps,
        "metrics": metrics or [],
        "notes": notes or [
            "示例系统画像保存在 data/sample_system_profile.json，修改很方便。",
            "三类检查共享同一份清单，但审查重点不同。",
            "最终会输出 JSON、Markdown 报告和章节得分图。",
        ],
    }
    OUTPUTS.mkdir(parents=True, exist_ok=True)
    PROGRESS_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def main():
    env = os.environ.copy()
    env.update(ensure_openai_credentials("zh"))
    env["PYTHONPATH"] = str(REPO_ROOT) + os.pathsep + env.get("PYTHONPATH", "")
    steps = []
    write_progress(steps)
    subprocess.run([sys.executable, str(ROOT / "src" / "generate_report.py")], cwd=ROOT, env=env, check=True)
    steps.append({"name": "运行隐私、可解释性和公平性检查", "status": "done", "detail": "src/generate_report.py"})
    report = json.loads((OUTPUTS / "compliance_report.json").read_text(encoding="utf-8"))
    metrics = [
        {"label": "总分", "value": f"{report['overall_score']}/{report['overall_max']}"},
        {"label": "等级", "value": report['overall_label']},
        {"label": "章节数", "value": str(len(report['sections']))},
        {"label": "需改进项", "value": str(report['action_required_count'])},
    ]
    write_progress(steps, metrics=metrics)
    subprocess.run([sys.executable, str(ROOT / "app" / "progress_dashboard.py")], cwd=ROOT, env=env, check=True)
    print("第 6 章演示运行完成。")


if __name__ == "__main__":
    main()
