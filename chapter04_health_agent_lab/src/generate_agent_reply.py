from dialog_state_tracker import update_state
from escalation_guard import should_escalate


def build_reply(user_text: str, prior_state: dict | None = None):
    state = update_state(prior_state or {}, user_text)
    if should_escalate(user_text, state):
        reply = (
            "听起来这是需要立即处理的身体信号。"
            " 我不能替代急诊判断，请现在尽快联系急救或让身边的人陪你去急诊。"
        )
        state["recommended_action"] = "urgent_handoff"
        return reply, state

    if state.get("need") == "routine_support":
        reply = (
            "谢谢你把这个困难说出来。"
            " 我建议先把吃药和每天固定动作绑定，例如早餐后或刷牙后立刻服药。"
            " 你更容易忘记的是早上还是晚上？"
        )
    elif state.get("emotion") == "distressed":
        reply = (
            "听起来你最近很累，也因为睡眠问题感到烦躁。"
            " 我建议先记录一周的睡眠时间和晚间刷手机情况，看看哪些时段最影响入睡。"
            " 最近这种情况出现多久了？"
        )
    else:
        reply = (
            "我理解你想先弄清楚发生了什么。"
            " 我可以帮你梳理下一步，但不能替代医生诊断。"
            " 先告诉我最困扰你的一个症状。"
        )
    state["recommended_action"] = "self_monitor_and_follow_up"
    return reply, state
