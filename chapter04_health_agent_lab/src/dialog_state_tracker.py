def update_state(prior_state, user_text):
    state = dict(prior_state)
    text = str(user_text)
    state["turn_count"] = state.get("turn_count", 0) + 1
    if any(keyword in text for keyword in ["烦躁", "担心", "压力", "累"]):
        state["emotion"] = "distressed"
    if any(keyword in text for keyword in ["忘记", "提醒"]):
        state["need"] = "routine_support"
    if any(keyword in text for keyword in ["胸口", "呼吸困难", "剧烈疼痛"]):
        state["risk_level"] = "high"
    elif any(keyword in text for keyword in ["头晕", "腿肿", "发作"]):
        state["risk_level"] = "medium"
    else:
        state.setdefault("risk_level", "low")
    state["last_user_text"] = text
    return state
