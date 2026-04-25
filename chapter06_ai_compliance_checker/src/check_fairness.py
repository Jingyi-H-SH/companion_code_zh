"""Review fairness monitoring and appeal mechanisms with a structured LLM rubric."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from shared.openai_utils import json_completion


SCHEMA = {
    "type": "object",
    "properties": {
        "section_summary": {"type": "string"},
        "findings": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "question": {"type": "string"},
                    "status": {"type": "string", "enum": ["pass", "partial", "action_required"]},
                    "score": {"type": "number"},
                    "evidence": {"type": "string"},
                    "recommended_action": {"type": "string"},
                },
                "required": ["id", "question", "status", "score", "evidence", "recommended_action"],
                "additionalProperties": False,
            },
        },
    },
    "required": ["section_summary", "findings"],
    "additionalProperties": False,
}


def run_fairness_check(system_profile: dict, checklist_items: list[dict]) -> dict:
    prompt = (
        f"System profile:\n{json.dumps(system_profile, ensure_ascii=False, indent=2)}\n\n"
        f"Checklist items:\n{json.dumps(checklist_items, ensure_ascii=False, indent=2)}\n\n"
        "Review fairness testing, monitoring, and appeal pathways. Score each item from 0 up to its weight."
    )
    result = json_completion(
        "You review fairness and governance practices for health AI systems. Return concise evidence-based JSON.",
        prompt,
        "fairness_review",
        SCHEMA,
    )
    total_score = 0.0
    findings = []
    for item, finding in zip(checklist_items, result["findings"]):
        score = max(0.0, min(float(item["weight"]), float(finding["score"])))
        total_score += score
        findings.append({**finding, "score": score, "weight": item["weight"]})
    return {"summary": result["section_summary"], "findings": findings, "score": total_score, "max_score": sum(item["weight"] for item in checklist_items)}
