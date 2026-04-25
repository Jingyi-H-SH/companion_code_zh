from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from shared.openai_utils import json_completion
from shared.rag_utils import format_chunks, load_json_items, retrieve_chunks


KB_PATH = ROOT / "chapter04_health_agent_lab" / "data" / "health_knowledge_base.json"
KNOWLEDGE_BASE = load_json_items(KB_PATH)
SCHEMA = {
    "type": "object",
    "properties": {
        "assistant_reply": {"type": "string"},
        "action_focus": {"type": "string"},
        "boundary_statement": {"type": "string"}
    },
    "required": ["assistant_reply", "action_focus", "boundary_statement"],
    "additionalProperties": False
}


def generate_reply(policy: dict, scenario_focus: str, conversation_text: str, state: dict, escalation: dict) -> dict:
    latest_user_message = conversation_text.strip().splitlines()[-1].replace("User: ", "", 1)
    retrieved = retrieve_chunks(f"{scenario_focus} {latest_user_message}", KNOWLEDGE_BASE, top_k=2)
    if escalation["needs_escalation"]:
        urgent_ids = [item["id"] for item in retrieved if item["id"] == "KB-URGENT"] or ["KB-URGENT"]
        return {
            "assistant_reply": (
                "Your symptoms sound urgent. Please seek immediate medical attention now or call emergency services, "
                "rather than waiting to see if the symptoms pass."
            ),
            "action_focus": "urgent_handoff",
            "boundary_statement": "This demo assistant cannot judge whether chest tightness and shortness of breath are safe to monitor at home.",
            "retrieved_reference_ids": urgent_ids,
        }
    prompt = (
        f"Teaching focus: {scenario_focus}\n"
        f"Conversation so far:\n{conversation_text}\n\n"
        f"State summary: {state}\n"
        f"Policy voice: {policy.get('voice')}\n"
        f"Must do: {policy.get('must_do')}\n"
        f"Must not do: {policy.get('must_not')}\n"
        f"Retrieved support notes:\n{format_chunks(retrieved)}\n\n"
        "Write one short, empathetic English reply."
    )
    result = json_completion(
        "You are a careful health support agent for a classroom simulation. Do not diagnose. Keep the tone warm and concise. Use the retrieved notes as grounding context.",
        prompt,
        "health_agent_reply",
        SCHEMA,
    )
    result["retrieved_reference_ids"] = [item["id"] for item in retrieved]
    return result
