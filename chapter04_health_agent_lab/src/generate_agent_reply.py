"""Generate an assistant reply while respecting the explicit safety rule."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from shared.openai_utils import json_completion


SCHEMA = {
    "type": "object",
    "properties": {
        "assistant_reply": {"type": "string"},
        "action_focus": {"type": "string"},
        "boundary_statement": {"type": "string"},
    },
    "required": ["assistant_reply", "action_focus", "boundary_statement"],
    "additionalProperties": False,
}


def generate_reply(policy: dict, scenario_focus: str, conversation_text: str, state: dict, escalation: dict) -> dict:
    if escalation["needs_escalation"]:
        return {
            "assistant_reply": (
                "Your symptoms sound urgent. Please seek immediate medical attention now or call emergency services, "
                "rather than waiting to see if the symptoms pass."
            ),
            "action_focus": "urgent_handoff",
            "boundary_statement": "This demo assistant cannot judge whether chest tightness and shortness of breath are safe to monitor at home.",
        }
    prompt = (
        f"Teaching focus: {scenario_focus}\n"
        f"Conversation so far:\n{conversation_text}\n\n"
        f"State summary: {state}\n"
        f"Policy voice: {policy.get('voice')}\n"
        f"Must do: {policy.get('must_do')}\n"
        f"Must not do: {policy.get('must_not')}\n"
        "Write one short, empathetic English reply."
    )
    return json_completion(
        "You are a careful health support agent for a classroom simulation. Do not diagnose. Keep the tone warm and concise.",
        prompt,
        "health_agent_reply",
        SCHEMA,
    )
