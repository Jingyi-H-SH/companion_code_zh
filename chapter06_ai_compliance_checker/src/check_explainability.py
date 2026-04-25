from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from shared.openai_utils import json_completion
from shared.rag_utils import format_chunks, load_json_items, retrieve_chunks


REFERENCE_PATH = ROOT / "chapter06_ai_compliance_checker" / "data" / "governance_reference.json"
REFERENCES = [item for item in load_json_items(REFERENCE_PATH) if item["section"] == "explainability"]
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
                    "recommended_action": {"type": "string"}
                },
                "required": ["id", "question", "status", "score", "evidence", "recommended_action"],
                "additionalProperties": False
            }
        }
    },
    "required": ["section_summary", "findings"],
    "additionalProperties": False
}


def run_explainability_check(system_profile: dict, checklist_items: list[dict]) -> dict:
    retrieved = retrieve_chunks(
        json.dumps(system_profile, ensure_ascii=False) + " " + " ".join(item["question"] for item in checklist_items),
        REFERENCES,
        top_k=2,
    )
    prompt = (
        f"System profile:\n{json.dumps(system_profile, ensure_ascii=False, indent=2)}\n\n"
        f"Checklist items:\n{json.dumps(checklist_items, ensure_ascii=False, indent=2)}\n\n"
        f"Retrieved governance references:\n{format_chunks(retrieved)}\n\n"
        "Score each item from 0 up to its weight and explain the evidence briefly."
    )
    result = json_completion(
        "You review explainability practices for health AI systems. Use the retrieved governance references as grounding context and return concise evidence-based JSON.",
        prompt,
        "explainability_review",
        SCHEMA,
    )
    total_score = 0.0
    findings = []
    for item, finding in zip(checklist_items, result["findings"]):
        score = max(0.0, min(float(item["weight"]), float(finding["score"])))
        total_score += score
        findings.append({**finding, "score": score, "weight": item["weight"]})
    return {
        "summary": result["section_summary"],
        "findings": findings,
        "score": total_score,
        "max_score": sum(item["weight"] for item in checklist_items),
        "retrieved_reference_ids": [item["id"] for item in retrieved],
    }
