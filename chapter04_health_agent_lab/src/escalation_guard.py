"""Keep the crisis handoff logic explicit so readers can inspect the safety rule."""

def check_escalation(message: str, policy: dict) -> dict:
    lowered = message.lower()
    hits = [keyword for keyword in policy.get("escalate_keywords", []) if keyword.lower() in lowered]
    return {
        "needs_escalation": bool(hits),
        "reason": ", ".join(hits) if hits else "",
    }
