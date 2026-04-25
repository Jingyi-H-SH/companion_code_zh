"""Summarize the user turn into a small state object for reply generation."""

def summarize_user_state(message: str) -> dict:
    lowered = message.lower()
    if any(term in lowered for term in ["chest", "cannot breathe", "short of breath", "severe pain"]):
        emotion = "distressed"
    elif any(term in lowered for term in ["sleep", "exhausted", "irritable", "stress"]):
        emotion = "overwhelmed"
    elif any(term in lowered for term in ["medicine", "blood pressure", "forgetting"]):
        emotion = "uncertain"
    else:
        emotion = "seeking_help"
    return {
        "emotion": emotion,
        "mentions_red_flag": any(term in lowered for term in ["chest", "short of breath", "fainted", "cannot breathe"]),
        "needs_practical_tip": any(term in lowered for term in ["how", "what", "simple", "try"]),
    }
