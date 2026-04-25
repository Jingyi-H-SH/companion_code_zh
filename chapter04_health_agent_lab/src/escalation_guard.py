import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY_PATH = ROOT / "prompts" / "agent_policies.yaml"


def load_policies():
    return json.loads(POLICY_PATH.read_text(encoding="utf-8"))


def should_escalate(user_text: str, state: dict) -> bool:
    policies = load_policies()
    if state.get("risk_level") == "high":
        return True
    return any(keyword in str(user_text) for keyword in policies["escalate_keywords"])
