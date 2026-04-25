import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
OUTPUTS = ROOT / "outputs"
PROGRESS_PATH = OUTPUTS / "progress.json"


def write_progress(steps, metrics=None, notes=None):
    payload = {
        "title": "第6章演示进度",
        "subtitle": "健康咨询AI伦理与治理自查",
        "steps": steps,
        "metrics": metrics or [],
        "notes": notes or [
            "清单条目都比较短，适合课堂上一条一条讨论。",
            "报告会直接指出系统在上线前还需要补哪些治理动作。",
            "教师可以直接替换 generate_report.py 中的系统画像进行扩展演示。",
        ],
    }
    OUTPUTS.mkdir(parents=True, exist_ok=True)
    PROGRESS_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def main():
    steps = []
    write_progress(steps)
    subprocess.run([sys.executable, str(ROOT / "src" / "generate_report.py")], cwd=ROOT, check=True)
    steps.append({"name": "执行隐私、可解释性与公平性检查", "status": "done", "detail": "src/generate_report.py"})
    report = json.loads((OUTPUTS / "compliance_report.json").read_text(encoding="utf-8"))
    metrics = [
        {"label": "总分", "value": f"{report['overall_score']}/{report['overall_max']}"},
        {"label": "状态", "value": report['overall_label']},
        {"label": "模块数", "value": str(len(report['sections']))},
    ]
    write_progress(steps, metrics=metrics)
    subprocess.run([sys.executable, str(ROOT / "app" / "progress_dashboard.py")], cwd=ROOT, check=True)
    print("第6章演示已完成。")


if __name__ == "__main__":
    main()
