import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from check_explainability import run_explainability_check
from check_fairness import run_fairness_check
from check_privacy import run_privacy_check
from load_checklist import load_checklist


REPORT_JSON = ROOT / "outputs" / "compliance_report.json"
REPORT_MD = ROOT / "outputs" / "compliance_report.md"

SAMPLE_SYSTEM = {
    "name": "健康咨询助手",
    "collects_minimum_data": True,
    "retention_policy": "",
    "consent_flow": True,
    "capability_statement": True,
    "shows_reasoning_basis": False,
    "human_handoff": True,
    "group_testing_complete": False,
    "post_deployment_monitoring": False,
    "appeal_path": True,
}


def label(score, max_score):
    ratio = score / max_score if max_score else 0
    if ratio >= 0.8:
        return "绿色"
    if ratio >= 0.5:
        return "黄色"
    return "红色"


def main() -> None:
    checklist = load_checklist()
    privacy = run_privacy_check(SAMPLE_SYSTEM, checklist["privacy"])
    explainability = run_explainability_check(SAMPLE_SYSTEM, checklist["explainability"])
    fairness = run_fairness_check(SAMPLE_SYSTEM, checklist["fairness"])
    sections = {
        "隐私保护": privacy,
        "可解释性": explainability,
        "公平性": fairness,
    }
    overall_score = sum(section["score"] for section in sections.values())
    overall_max = sum(section["max_score"] for section in sections.values())
    payload = {
        "system_name": SAMPLE_SYSTEM["name"],
        "sections": sections,
        "overall_score": overall_score,
        "overall_max": overall_max,
        "overall_label": label(overall_score, overall_max),
    }
    REPORT_JSON.parent.mkdir(parents=True, exist_ok=True)
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        f"# 合规自查报告：{SAMPLE_SYSTEM['name']}",
        "",
        f"总分：{overall_score}/{overall_max}（{payload['overall_label']}）",
        "",
    ]
    for section_name, section in sections.items():
        lines.append(f"## {section_name}")
        lines.append(f"得分：{section['score']}/{section['max_score']}")
        for finding in section["findings"]:
            lines.append(f"- {'通过' if finding['passed'] else '待改进'}：{finding['question']}")
        lines.append("")
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"已保存合规自查报告：{REPORT_JSON}")


if __name__ == "__main__":
    main()
