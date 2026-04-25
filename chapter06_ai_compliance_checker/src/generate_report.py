"""Run the three section checks and build a final reader-facing report."""

from __future__ import annotations

import json
import sys
from pathlib import Path
import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from chapter06_ai_compliance_checker.src.check_explainability import run_explainability_check
from chapter06_ai_compliance_checker.src.check_fairness import run_fairness_check
from chapter06_ai_compliance_checker.src.check_privacy import run_privacy_check
from chapter06_ai_compliance_checker.src.load_checklist import load_checklist


CHAPTER_ROOT = ROOT / "chapter06_ai_compliance_checker"
PROFILE_PATH = CHAPTER_ROOT / "data" / "sample_system_profile.json"
REPORT_JSON = CHAPTER_ROOT / "outputs" / "compliance_report.json"
REPORT_MD = CHAPTER_ROOT / "outputs" / "compliance_report.md"
FIG_PATH = CHAPTER_ROOT / "outputs" / "section_scores.png"


def label(score: float, max_score: float) -> str:
    ratio = score / max_score if max_score else 0.0
    if ratio >= 0.8:
        return "strong"
    if ratio >= 0.5:
        return "mixed"
    return "needs_attention"


def main() -> None:
    checklist = load_checklist()
    system_profile = json.loads(PROFILE_PATH.read_text(encoding="utf-8"))
    sections = {
        "privacy": run_privacy_check(system_profile, checklist["privacy"]),
        "explainability": run_explainability_check(system_profile, checklist["explainability"]),
        "fairness": run_fairness_check(system_profile, checklist["fairness"]),
    }
    overall_score = sum(section["score"] for section in sections.values())
    overall_max = sum(section["max_score"] for section in sections.values())
    action_required_count = sum(
        finding["status"] == "action_required"
        for section in sections.values()
        for finding in section["findings"]
    )
    payload = {
        "system_name": system_profile["name"],
        "sections": sections,
        "overall_score": overall_score,
        "overall_max": overall_max,
        "overall_label": label(overall_score, overall_max),
        "action_required_count": action_required_count,
    }
    REPORT_JSON.parent.mkdir(parents=True, exist_ok=True)
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        f"# Compliance Review: {system_profile['name']}",
        "",
        f"- Overall score: {overall_score:.1f}/{overall_max:.1f}",
        f"- Overall label: {payload['overall_label']}",
        f"- Action-required findings: {action_required_count}",
        "",
    ]
    for section_name, section in sections.items():
        lines.append(f"## {section_name.title()}")
        lines.append(section["summary"])
        lines.append(f"Score: {section['score']:.1f}/{section['max_score']:.1f}")
        for finding in section["findings"]:
            lines.append(f"- {finding['status'].upper()}: {finding['question']} | score {finding['score']}/{finding['weight']} | {finding['recommended_action']}")
        lines.append("")
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")

    names = list(sections.keys())
    scores = [sections[name]["score"] for name in names]
    max_scores = [sections[name]["max_score"] for name in names]
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.bar(names, scores, color="#3c8dbc", label="Score")
    ax.plot(names, max_scores, color="#dd4b39", marker="o", label="Max")
    ax.set_ylabel("Score")
    ax.legend()
    fig.tight_layout()
    fig.savefig(FIG_PATH, dpi=180)
    print(f"Saved {REPORT_JSON}, {REPORT_MD}, and {FIG_PATH}")


if __name__ == "__main__":
    main()
